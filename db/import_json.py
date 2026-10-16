"""Create the SQLite schema and import the legacy JSON data."""

import json
import sqlite3

from db.database import BASE_DIR, DATABASE_PATH


SCHEMA_PATH = BASE_DIR / 'sql' / 'schema.sql'
DATA_PATH = BASE_DIR / 'data'


def read_json(filename: str) -> list[dict]:
    """Read a JSON collection from the project's data directory."""
    with (DATA_PATH / filename).open(encoding='utf-8') as source:
        return json.load(source)


def import_json_data() -> None:
    """Replace the application tables with the current JSON collections."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
        with connection:
            connection.execute('DELETE FROM bookings')
            connection.execute('DELETE FROM rooms')
            connection.execute('DELETE FROM users')
            connection.executemany(
                'INSERT INTO rooms (id, name, capacity) VALUES (?, ?, ?)',
                [
                    (room['id'], room['name'], room['capacity'])
                    for room in read_json('rooms.json')
                ],
            )
            connection.executemany(
                'INSERT INTO users (id, name, email) VALUES (?, ?, ?)',
                [
                    (user['id'], user['name'], user['email'])
                    for user in read_json('users.json')
                ],
            )
            connection.executemany(
                'INSERT INTO bookings '
                '(id, room_id, booking_date, user_id, is_cancelled) '
                'VALUES (?, ?, ?, ?, ?)',
                [
                    (
                        booking['id'],
                        booking['room_id'],
                        booking['booking_date'],
                        booking['user_id'],
                        int(booking.get('is_cancelled', False)),
                    )
                    for booking in read_json('bookings.json')
                ],
            )
    finally:
        connection.close()


if __name__ == '__main__':
    import_json_data()
    print(f'Импорт завершён: {DATABASE_PATH}')
