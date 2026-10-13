from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.bookings import is_room_available
from models.rooms import find_room_by_id
from storage import load_bookings, load_rooms, load_users


def rooms(request):
    items = ''
    for room in load_rooms('data/rooms.json'):
        text = f'{room.name} - вместимость {room.capacity} мест'
        items += f'<li class="list-group-item">{text}</li>'
    content = f"""
    <h1>Помещения</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('Roomly - помещения', content))


def room_detail(request, room_id):
    rooms_list = load_rooms('data/rooms.json')
    room = find_room_by_id(rooms_list, room_id)
    if room is None:
        content = """
        <h1 class="text-danger">Помещение не найдено</h1>
        <a href="/rooms/" class="btn btn-outline-secondary">
        ← к списку помещений</a>
        """
        return HttpResponse(
            page('Помещение не найдено', content),
            status=404,
        )
    users_list = load_users('data/users.json')
    bookings_list = load_bookings(
        'data/bookings.json', rooms_list, users_list,
    )
    available = is_room_available(bookings_list, room, date.today())
    status = 'доступно' if available else 'занято'
    badge = 'bg-success' if available else 'bg-danger'
    content = f"""
    <div class="card">
    <div class="card-body">
    <h5 class="card-title">{room.name}</h5>
    <p class="card-text"><strong>ID:</strong> {room.id}</p>
    <p class="card-text">
    <strong>Вместимость:</strong> {room.capacity} мест
    </p>
    <p class="card-text">
    Доступность: <span class="badge {badge}">{status}</span>
    </p>
    <a href="/rooms/" class="btn btn-outline-secondary">
    ← к списку помещений</a>
    </div>
    </div>
    """
    return HttpResponse(page(room.name, content))
