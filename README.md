# Roomly — сервис поиска свободных аудиторий

Консольное приложение для учёта аудиторного фонда и бронирования
помещений, дополненное веб-интерфейсом на Django.

## Возможности

- просмотр и поиск аудиторий;
- проверка вместимости и доступности на дату;
- создание и отмена бронирований;
- работа с пользователями;
- веб-интерфейс на Django-шаблонах;
- сохранение данных в JSON между запусками.

## Технологии

- Python 3.11
- Django 5.2 (Django Template Language)
- HTML5, CSS3, Bootstrap 5.3
- JavaScript
- JSON (хранение данных)
- pytest, flake8

## Страницы веб-интерфейса

| URL                           | Назначение               |
| ----------------------------- | ------------------------ |
| `/`                           | Главная страница         |
| `/rooms/`                     | Список аудиторий         |
| `/rooms/<int:room_id>/`       | Карточка аудитории       |
| `/bookings/`                  | Список бронирований      |
| `/bookings/<int:booking_id>/` | Карточка бронирования    |
| любой несуществующий          | Собственная страница 404 |

## Структура проекта

room-booking-service/
├── manage.py
├── requirements.txt
├── roomly/ # конфигурация Django-проекта
├── templates/ # шаблоны уровня проекта
│ ├── base.html
│ ├── 404.html
│ └── includes/navigation.html
├── homepage/ # приложение: главная
│ ├── templates/homepage/index.html
│ └── static/homepage/ # CSS, JS, логотип
├── rooms/ # приложение: аудитории
│ └── templates/rooms/
│ ├── room_list.html
│ ├── room_detail.html
│ └── includes/room_card.html
├── bookings/ # приложение: бронирования
│ └── templates/bookings/
│ ├── booking_list.html
│ ├── booking_detail.html
│ └── includes/booking_status.html
├── models/ # классы Room, User, Booking (ПР3)
├── data/ # rooms.json, users.json, bookings.json
├── tests/ # тесты pytest
├── storage.py # загрузка/сохранение JSON
└── main.py # консольная версия (сохранена)

## Django-шаблоны

- **`base.html`** — общая структура страниц с блоками `title` и `content`.
- **Наследование** — через `{% extends %}` и `{% block %}`.
- **Включаемые шаблоны** — навигация, карточка аудитории, статус брони.
- **Контекст** — данные передаются в шаблоны через словарь.
- **Циклы и условия** — `{% for %}`, `{% empty %}`, `{% if %}`.
- **Фильтры** — `{{ rooms|length }}`, `{{ room.name|default:"Без названия" }}`.
- **Ссылки** — через `{% url %}` с пространствами имён.
- **Статика** — через `{% static %}`.

## Требования

- Python 3.11+
- Django 5.2
- pytest
- flake8

Установка:

pip install -r requirements.txt
Запуск
Веб-версия:

python manage.py migrate
python manage.py runserver
Открыть: http://127.0.0.1:8000/

Консольная версия:

bash
python main.py
Тестирование и проверка
bash
python -m pytest -v
python -m flake8 . --extend-exclude=venv
Хранение данных
Данные хранятся в JSON-файлах data/rooms.json, data/users.json,
data/bookings.json. Django ORM и база данных пока не используются —
переход запланирован на ПР7.

Текущее состояние
Реализовано:

классы Room, User, Booking;

Django-проект и три приложения;

шаблонный веб-интерфейс с базовым шаблоном и наследованием;

циклы, условия, фильтры, именованные URL;

собственные CSS, JavaScript, логотип;

собственная страница 404;

консольная версия и тесты ПР3 сохранены.

Планируется:

переход на Django ORM и базу данных;

Django Forms;

## SQL project (PR7)

This section supersedes the earlier planned-status notes below the original
project description.

The Django web app now reads its application data from `data/roomly.sqlite` via
the built-in `sqlite3` module. The console app and JSON source files remain
available.

For the first web app launch, create the SQLite schema and import the JSON data:

```powershell
python -m db.import_json
python manage.py migrate
python manage.py runserver
```

Re-run `python -m db.import_json` to reload `rooms`, `users`, and `bookings` from
their JSON files. Django's own `db.sqlite3` is separate.

The web app includes `/rooms/`, `/bookings/`, `/rooms/available/?date=YYYY-MM-DD`,
and `/bookings/statistics/`. Booking pages use SQL joins; room availability is
filtered by date; statistics use `COUNT` and `GROUP BY`.

- `sql/schema.sql` creates tables, foreign keys, constraints, and indexes.
- `db/import_json.py` imports JSON into SQLite.
- `db/database.py` opens connections with `sqlite3.Row` and foreign keys enabled.
- `sql/queries.sql` contains `WHERE`, `JOIN`, `COUNT`, and `GROUP BY` examples.

Validation commands: `python manage.py check`, `python -m pytest -v`, and
`python -m flake8 . --extend-exclude=venv`.

аутентификация пользователей;

REST API и контейнеризация.
