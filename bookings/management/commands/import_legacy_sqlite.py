"""Copy data from the PR7 SQLite schema into Django ORM tables."""

import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bookings.models import Booking, User
from rooms.models import Room


class Command(BaseCommand):
    help = 'Импортировать помещения, пользователей и бронирования из SQLite ПР7.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            default=str(settings.BASE_DIR / 'data' / 'roomly.sqlite'),
            help='Путь к SQLite-базе ПР7 (по умолчанию data/roomly.sqlite).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source = options['source']
        try:
            connection = sqlite3.connect(source)
            connection.row_factory = sqlite3.Row
            rooms = connection.execute(
                'SELECT id, name, capacity FROM rooms ORDER BY id'
            ).fetchall()
            users = connection.execute(
                'SELECT id, name, email FROM users ORDER BY id'
            ).fetchall()
            bookings = connection.execute(
                'SELECT id, room_id, user_id, booking_date, is_cancelled '
                'FROM bookings ORDER BY id'
            ).fetchall()
        except (sqlite3.Error, OSError) as error:
            raise CommandError(f'Не удалось прочитать {source}: {error}') from error
        finally:
            if 'connection' in locals():
                connection.close()

        for row in rooms:
            Room.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'name': row['name'],
                    'capacity': row['capacity'],
                    'slug': '',
                },
            )
        for row in users:
            User.objects.update_or_create(
                pk=row['id'],
                defaults={'name': row['name'], 'email': row['email']},
            )
        for row in bookings:
            Booking.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'room_id': row['room_id'],
                    'user_id': row['user_id'],
                    'booking_date': row['booking_date'],
                    'status': (
                        Booking.Status.CANCELLED if row['is_cancelled']
                        else Booking.Status.ACTIVE
                    ),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f'Импортировано: помещений — {len(rooms)}, '
            f'пользователей — {len(users)}, бронирований — {len(bookings)}.'
        ))
