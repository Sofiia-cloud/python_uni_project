from django.shortcuts import render

from db.database import get_connection


def rooms(request):
    with get_connection() as connection:
        rooms_list = connection.execute(
            'SELECT id, name, capacity FROM rooms ORDER BY name'
        ).fetchall()
    return render(request, 'rooms/room_list.html', {'rooms': rooms_list})


def room_detail(request, room_id):
    with get_connection() as connection:
        room = connection.execute(
            'SELECT id, name, capacity FROM rooms WHERE id = ?',
            (room_id,),
        ).fetchone()
    return render(
        request,
        'rooms/room_detail.html',
        {'room': room},
        status=404 if room is None else 200,
    )


def available(request):
    """Show rooms that are free on the date supplied in the query string."""
    booking_date = request.GET.get('date', '')
    available_rooms = []
    if booking_date:
        with get_connection() as connection:
            available_rooms = connection.execute(
                '''SELECT id, name, capacity
                   FROM rooms
                   WHERE id NOT IN (
                       SELECT room_id FROM bookings
                       WHERE booking_date = ? AND is_cancelled = 0
                   )
                   ORDER BY name''',
                (booking_date,),
            ).fetchall()
    return render(
        request,
        'rooms/available.html',
        {'rooms': available_rooms, 'booking_date': booking_date},
    )
