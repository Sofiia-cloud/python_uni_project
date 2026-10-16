-- Rooms with a minimum capacity, ordered from the largest.
SELECT id, name, capacity
FROM rooms
WHERE capacity >= ?
ORDER BY capacity DESC, name;

-- Active bookings with the associated room and user.
SELECT bookings.id, bookings.booking_date, bookings.is_cancelled,
       rooms.id AS room_id, rooms.name AS room_name,
       users.id AS user_id, users.name AS user_name, users.email AS user_email
FROM bookings
JOIN rooms ON bookings.room_id = rooms.id
JOIN users ON bookings.user_id = users.id
WHERE bookings.is_cancelled = 0
ORDER BY bookings.booking_date, bookings.id;

-- Rooms that are free on the requested date.
SELECT rooms.id, rooms.name, rooms.capacity
FROM rooms
WHERE rooms.id NOT IN (
    SELECT bookings.room_id
    FROM bookings
    WHERE bookings.booking_date = ?
      AND bookings.is_cancelled = 0
)
ORDER BY rooms.name;

-- Booking totals per room, including rooms without bookings.
SELECT rooms.id AS room_id, rooms.name AS room_name,
       COUNT(bookings.id) AS bookings_count
FROM rooms
LEFT JOIN bookings
       ON rooms.id = bookings.room_id
      AND bookings.is_cancelled = 0
GROUP BY rooms.id, rooms.name
ORDER BY bookings_count DESC, rooms.name;
