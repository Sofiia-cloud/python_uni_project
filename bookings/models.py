from django.db import models
from django.db.models import Count, Q
from django.urls import reverse

from rooms.models import Room


class User(models.Model):
    name = models.CharField('Имя', max_length=120)
    email = models.EmailField('Электронная почта', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.name


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Booking.Status.ACTIVE)

    def for_date(self, booking_date):
        return self.filter(booking_date=booking_date)

    def with_relations(self):
        return self.select_related('room', 'user')


class Booking(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активно'
        CANCELLED = 'cancelled', 'Отменено'
        COMPLETED = 'completed', 'Завершено'

    room = models.ForeignKey(
        Room, on_delete=models.PROTECT, related_name='bookings',
        verbose_name='Помещение',
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='bookings',
        verbose_name='Пользователь',
    )
    booking_date = models.DateField('Дата бронирования')
    status = models.CharField(
        'Статус', max_length=12, choices=Status.choices,
        default=Status.ACTIVE,
    )

    objects = BookingQuerySet.as_manager()

    class Meta:
        ordering = ('-booking_date', '-id')
        verbose_name = 'бронирование'
        verbose_name_plural = 'бронирования'
        indexes = [
            models.Index(fields=('booking_date', 'status')),
            models.Index(fields=('room', 'booking_date', 'status')),
        ]

    def __str__(self):
        return f'{self.room.name} — {self.booking_date} ({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse('bookings:detail', kwargs={'booking_id': self.pk})

    @classmethod
    def room_statistics(cls):
        return Room.objects.annotate(
            bookings_count=Count(
                'bookings', filter=Q(bookings__status=cls.Status.ACTIVE)
            ),
        ).order_by('-bookings_count', 'name')
