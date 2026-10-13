# Roomly — сервис поиска свободных аудиторий

Приложение для учёта аудиторного фонда учебного заведения
и бронирования помещений. Консольная версия (ПР3) дополнена
веб-интерфейсом на Django (ПР5).

## Возможности

- просмотр списка аудиторий в браузере;
- просмотр информации об отдельной аудитории;
- просмотр списка бронирований;
- просмотр информации об отдельном бронировании;
- проверка доступности аудитории на текущую дату;
- навигация между страницами;
- обработка несуществующих адресов и объектов (страница 404);
- сохранение данных в JSON-файлах между запусками.

## Используемые технологии

- Python 3.11
- Django 5.2 — веб-фреймворк
- HTML — разметка страниц
- CSS и Bootstrap 5.3 — оформление
- pytest — автоматизированные тесты
- flake8 — проверка качества кода

## Предметная область

Основные сущности:

- **Room** — аудитория;
- **User** — пользователь системы;
- **Booking** — бронирование аудитории пользователем.

`Booking` связывает `Room` и `User`. На одну дату у одной аудитории
может быть только одно активное бронирование. Отменённое бронирование
не блокирует аудиторию.

## Основные классы (ПР3)

### Room — аудитория

Атрибуты: `id`, `name`, `capacity`.

Методы:

- `is_suitable_for(people_count)` — проверка вместимости;
- `__str__()` — строковое представление.

### User — пользователь

Атрибуты: `id`, `name`, `email`.

Методы:

- `from_data(data)` — создание из словаря (`@classmethod`);
- `__str__()` — строковое представление.

### Booking — бронирование

Атрибуты: `id`, `room`, `booking_date`, `user`, `is_cancelled`.

Методы:

- `cancel()` — отмена бронирования;
- `__str__()` — строковое представление.

## Страницы веб-интерфейса (ПР5)

| URL                           | View-функция                    | Назначение                                           |
| ----------------------------- | ------------------------------- | ---------------------------------------------------- |
| `/`                           | `homepage.views.index`          | Главная страница, описание и навигация               |
| `/rooms/`                     | `rooms.views.rooms`             | Список аудиторий                                     |
| `/rooms/<int:room_id>/`       | `rooms.views.room_detail`       | Информация об аудитории, доступность на текущую дату |
| `/bookings/`                  | `bookings.views.bookings`       | Список бронирований                                  |
| `/bookings/<int:booking_id>/` | `bookings.views.booking_detail` | Информация о бронировании                            |
| любой несуществующий          | `homepage.views.page_not_found` | Собственная страница 404                             |

## Структура проекта

room-booking-service/
├── manage.py # управление Django-проектом
├── requirements.txt # зависимости проекта
├── README.md
├── .gitignore
├── .flake8 # настройки flake8
│
├── roomly/ # пакет конфигурации Django-проекта
│ ├── init.py
│ ├── settings.py # настройки проекта
│ ├── urls.py # корневая маршрутизация
│ ├── asgi.py
│ └── wsgi.py
│
├── homepage/ # Django-приложение: главная
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations/
│ ├── models.py
│ ├── tests.py
│ ├── urls.py # маршруты приложения
│ └── views.py # page(), index(), page_not_found()
│
├── rooms/ # Django-приложение: аудитории
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations/
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py # rooms(), room_detail()
│
├── bookings/ # Django-приложение: бронирования
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations/
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py # bookings(), booking_detail()
│
├── models/ # пакет ПР3: классы предметной области
│ ├── init.py
│ ├── rooms.py # класс Room и функции
│ ├── users.py # класс User и функции
│ └── bookings.py # класс Booking и функции
│
├── data/ # JSON-хранилище (ПР2–ПР3)
│ ├── rooms.json
│ ├── users.json
│ └── bookings.json
│
├── tests/ # тесты pytest (ПР3)
│ ├── test_rooms.py
│ ├── test_users.py
│ └── test_bookings.py
│
├── storage.py # загрузка и сохранение JSON
├── utils.py # вспомогательные функции ввода
└── main.py # консольная версия приложения (ПР3)

## Назначение модулей

### `roomly/`

Пакет настроек Django-проекта:

- `settings.py` — настройки: `INSTALLED_APPS`, локализация, отладка;
- `urls.py` — корневая маршрутизация и `handler404`.

### `homepage/`

Django-приложение, отвечающее за главную страницу:

- `page(title, content)` — единый HTML-каркас всех страниц проекта;
- `index(request)` — главная страница `/`;
- `page_not_found(request, exception)` — собственная страница 404.

### `rooms/`

Django-приложение для работы с аудиториями:

- `rooms(request)` — страница `/rooms/`;
- `room_detail(request, room_id)` — страница `/rooms/<id>/`.

### `bookings/`

Django-приложение для работы с бронированиями:

- `bookings(request)` — страница `/bookings/`;
- `booking_detail(request, booking_id)` — страница `/bookings/<id>/`;
- `find_booking_by_id(bookings, booking_id)` — поиск брони по id.

### `models/`

Пакет предметной области из ПР3:

- `rooms.py` — класс `Room` и функции работы с аудиториями;
- `users.py` — класс `User` и функции работы с пользователями;
- `bookings.py` — класс `Booking` и функции работы с бронями.

### `storage.py`

Загрузка и сохранение данных в JSON:

- `load_rooms()` / `save_rooms()` — для аудиторий;
- `load_users()` / `save_users()` — для пользователей;
- `load_bookings()` / `save_bookings()` — для броней.

При загрузке JSON-данные преобразуются в объекты `Room`, `User`, `Booking`;
при сохранении объекты преобразуются обратно в JSON.

### `utils.py`

Вспомогательные функции ввода:

- `input_int(prompt)` — безопасный ввод целого числа;
- `input_date(prompt)` — безопасный ввод даты.

### `main.py`

Консольная версия приложения (сохранена с ПР3). Запускается
параллельно с веб-интерфейсом.

### `tests/`

Автоматизированные тесты `pytest` для классов и функций ПР3.

## Требования

- Python 3.11+
- Django 5.2
- pytest
- flake8

Установка зависимостей:
pip install -r requirements.txt

## Запуск

### Веб-версия (Django)

python manage.py migrate
python manage.py runserver

Открыть в браузере: <http://127.0.0.1:8000/>

Основные страницы:

- <http://127.0.0.1:8000/> — главная;
- <http://127.0.0.1:8000/rooms/> — список аудиторий;
- <http://127.0.0.1:8000/rooms/1/> — аудитория;
- <http://127.0.0.1:8000/bookings/> — список броней;
- <http://127.0.0.1:8000/bookings/1/> — бронирование.

### Консольная версия (сохранена с ПР3)

python main.py

## Тестирование

python -m pytest -v

## Проверка качества кода

python -m flake8 . --extend-exclude=venv

## Формат хранения данных

- `data/rooms.json` — список аудиторий (`id`, `name`, `capacity`);
- `data/users.json` — список пользователей (`id`, `name`, `email`);
- `data/bookings.json` — список броней (`id`, `room_id`, `booking_date`,
  `user_id`, `is_cancelled`).

Отменённое бронирование не удаляется из файла, а помечается
`is_cancelled = true`.

## Текущее состояние

Реализовано:

- Django-проект `roomly` и три приложения: `homepage`, `rooms`, `bookings`;
- двухуровневая маршрутизация URL (`include()` + локальные `urls.py`);
- конвертеры путей `<int:room_id>`, `<int:booking_id>`;
- view-функции `index()`, `rooms()`, `room_detail()`, `bookings()`,
  `booking_detail()`;
- общий HTML-каркас `page()` с подключением Bootstrap 5.3;
- собственная обработка ошибки 404;
- отображение данных из JSON через объекты ПР3;
- навигация между страницами;
- сохранена консольная версия ПР3;
- тесты `pytest` проходят, `flake8` без замечаний.

## План развития

- перенос сущностей `Room`, `User`, `Booking` в Django ORM;
- подключение базы данных;
- переход на Django-шаблоны (`templates/`) и отказ от функции `page()`;
- реализация форм создания и редактирования броней;
- аутентификация и разграничение доступа;
- разработка REST API;
- контейнеризация в Docker;
- настройка CI/CD.
