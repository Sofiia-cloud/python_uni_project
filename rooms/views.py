from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from .forms import RoomForm
from .models import Room


def rooms(request):
    room_list = Room.objects.annotate(
        active_bookings_count=Count(
            'bookings', filter=Q(bookings__status=Booking.Status.ACTIVE)
        ),
    ).order_by('name')
    return render(request, 'rooms/room_list.html', {'rooms': room_list})


def room_detail(request, slug):
    room = get_object_or_404(
        Room.objects.prefetch_related('bookings__user'), slug=slug
    )
    return render(request, 'rooms/room_detail.html', {'room': room})


def room_detail_by_id(request, room_id):
    """Keep links from the PR7 interface working during the transition."""
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'rooms/room_detail.html', {'room': room})


def room_create(request):
    form = RoomForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(
        request, 'rooms/room_form.html',
        {'form': form, 'heading': 'Добавить помещение'},
    )


def room_edit(request, slug):
    room = get_object_or_404(Room, slug=slug)
    form = RoomForm(request.POST or None, request.FILES or None, instance=room)
    if request.method == 'POST' and form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(
        request, 'rooms/room_form.html',
        {'form': form, 'room': room, 'heading': f'Изменить: {room.name}'},
    )


def available(request):
    """Show rooms not occupied by an active booking on the selected date."""
    booking_date = request.GET.get('date', '')
    available_rooms = Room.objects.none()
    if booking_date:
        available_rooms = Room.objects.exclude(
            bookings__booking_date=booking_date,
            bookings__status=Booking.Status.ACTIVE,
        ).order_by('name').distinct()
    return render(
        request,
        'rooms/available.html',
        {'rooms': available_rooms, 'booking_date': booking_date},
    )
