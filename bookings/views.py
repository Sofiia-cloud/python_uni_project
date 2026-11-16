from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from rooms.models import Room
from .forms import BookingFilterForm, BookingForm
from .models import Booking


def bookings(request):
    form = BookingFilterForm(request.GET or None)
    booking_list = Booking.objects.with_relations()
    if form.is_valid():
        search = form.cleaned_data.get('search')
        booking_date = form.cleaned_data.get('booking_date')
        room = form.cleaned_data.get('room')
        status = form.cleaned_data.get('status')
        if search:
            booking_list = booking_list.filter(
                Q(room__name__icontains=search)
                | Q(user__name__icontains=search)
                | Q(user__email__icontains=search)
            )
        if booking_date:
            booking_list = booking_list.filter(booking_date=booking_date)
        if room:
            booking_list = booking_list.filter(room=room)
        if status:
            booking_list = booking_list.filter(status=status)

    sort = request.GET.get('sort', '-booking_date')
    sort_fields = {
        'booking_date': 'booking_date',
        '-booking_date': '-booking_date',
        'room': 'room__name',
        '-room': '-room__name',
        'user': 'user__name',
        '-user': '-user__name',
    }
    sort = sort if sort in sort_fields else '-booking_date'
    booking_list = booking_list.order_by(sort_fields[sort], '-id')
    page_obj = Paginator(booking_list, 10).get_page(request.GET.get('page'))
    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_params.pop('sort', None)
    return render(
        request,
        'bookings/booking_list.html',
        {'bookings': page_obj, 'page_obj': page_obj, 'filter_form': form,
         'sort': sort, 'query_params': query_params.urlencode()},
    )


def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.with_relations(), pk=booking_id
    )
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


def booking_create(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save()
        return redirect(booking.get_absolute_url())
    return render(
        request, 'bookings/booking_form.html',
        {'form': form, 'heading': 'Новое бронирование'},
    )


def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking.objects.with_relations(), pk=booking_id)
    form = BookingForm(request.POST or None, instance=booking)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(booking.get_absolute_url())
    return render(
        request, 'bookings/booking_form.html',
        {'form': form, 'heading': f'Редактировать бронирование №{booking.pk}',
         'booking': booking},
    )


@require_POST
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status == Booking.Status.ACTIVE:
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=('status',))
    return redirect(booking.get_absolute_url())


def statistics(request):
    room_statistics = Room.objects.annotate(
        bookings_count=Count(
            'bookings', filter=Q(bookings__status=Booking.Status.ACTIVE)
        ),
    ).order_by('-bookings_count', 'name')
    status_counts = {
        status: Booking.objects.filter(status=status).count()
        for status, _label in Booking.Status.choices
    }
    totals = Booking.objects.aggregate(
        total=Count('pk'),
        active=Count('pk', filter=Q(status=Booking.Status.ACTIVE)),
    )
    return render(
        request,
        'bookings/statistics.html',
        {'statistics': room_statistics, 'status_counts': status_counts,
         'totals': totals},
    )
