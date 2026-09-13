from datetime import date, time


# Данные об аудитории
room_number = 'А-301'
room_capacity = 30
room_building = 'Корпус А'
room_has_projector = True

# Данные о запросе на бронирование
requested_date = date(2026, 9, 15)
requested_start = time(14, 0)
requested_end = time(15, 30)
requested_people = 25

# Данные о существующем занятии в этой аудитории
existing_lesson_date = date(2026, 9, 15)
existing_lesson_start = time(13, 30)
existing_lesson_end = time(15, 0)

# Проверка пересечения по времени:
# занятие пересекается с запросом, если начало запроса раньше конца занятия
# и конец запроса позже начала занятия.
time_overlap = (
    requested_date == existing_lesson_date
    and requested_start < existing_lesson_end
    and requested_end > existing_lesson_start
)

# Проверка вместимости
capacity_ok = requested_people <= room_capacity

# Проверка наличия проектора (если нужно больше 20 человек — желателен проектор)
projector_ok = requested_people <= 20 or room_has_projector

can_book = not time_overlap and capacity_ok and projector_ok

print(f'Аудитория: {room_number} ({room_building})')
print(f'Вместимость: {room_capacity} мест')
print(f'Проектор: {"есть" if room_has_projector else "нет"}')
print()
print(f'Запрос на бронирование:')
print(f'  Дата: {requested_date}')
print(f'  Время: {requested_start}–{requested_end}')
print(f'  Количество человек: {requested_people}')
print()
print(f'Пересечение с занятием: {"да" if time_overlap else "нет"}')
print(f'Достаточно мест: {"да" if capacity_ok else "нет"}')
print(f'Условия по оборудованию: {"выполнены" if projector_ok else "не выполнены"}')
print()
print(f'Бронирование возможно: {"ДА" if can_book else "НЕТ"}')