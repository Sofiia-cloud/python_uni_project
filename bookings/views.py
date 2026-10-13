from django.http import HttpResponse

from homepage.views import page
from storage import load_bookings, load_rooms, load_users


def find_booking_by_id(bookings, booking_id):
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    return None


def bookings(request):
    rooms_list = load_rooms('data/rooms.json')
    users_list = load_users('data/users.json')
    bookings_list = load_bookings(
        'data/bookings.json', rooms_list, users_list,
    )
    items = ''
    for booking in bookings_list:
        status = 'отменено' if booking.is_cancelled else 'активно'
        badge = 'bg-secondary' if booking.is_cancelled else 'bg-success'
        text = f'{booking.room.name} - {booking.booking_date}'
        items += (
            f'<li class="list-group-item">'
            f'<a href="/bookings/{booking.id}/">{text}</a> '
            f'<span class="badge {badge}">{status}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Бронирования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('Roomly - бронирования', content))


def booking_detail(request, booking_id):
    rooms_list = load_rooms('data/rooms.json')
    users_list = load_users('data/users.json')
    bookings_list = load_bookings(
        'data/bookings.json', rooms_list, users_list,
    )
    booking = find_booking_by_id(bookings_list, booking_id)
    if booking is None:
        content = """
        <h1 class="text-danger">Бронирование не найдено</h1>
        <a href="/bookings/" class="btn btn-outline-secondary">
        ← к списку бронирований</a>
        """
        return HttpResponse(
            page('Бронирование не найдено', content),
            status=404,
        )
    status = 'отменено' if booking.is_cancelled else 'активно'
    badge = 'bg-secondary' if booking.is_cancelled else 'bg-success'
    content = f"""
    <div class="card">
    <div class="card-body">
    <h5 class="card-title">Бронирование №{booking.id}</h5>
    <p class="card-text">Помещение: {booking.room.name}</p>
    <p class="card-text">Дата: {booking.booking_date}</p>
    <p class="card-text">Пользователь: {booking.user.name}</p>
    <p class="card-text">
    Статус: <span class="badge {badge}">{status}</span>
    </p>
    <a href="/bookings/" class="btn btn-outline-secondary">
    ← к списку бронирований</a>
    </div>
    </div>
    """
    return HttpResponse(
        page(f'Бронирование №{booking.id}', content),
    )
