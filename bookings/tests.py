from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from rooms.models import Room
from .forms import BookingForm
from .models import Booking, User


class BookingWorkflowTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='Тестовая аудитория', capacity=20)
        self.other_room = Room.objects.create(name='Другая аудитория', capacity=12)
        self.user = User.objects.create(name='Тестовый пользователь', email='test@example.com')
        self.booking_date = date.today() + timedelta(days=5)
        self.booking = Booking.objects.create(
            room=self.room, user=self.user, booking_date=self.booking_date,
        )

    def test_booking_form_rejects_past_date(self):
        form = BookingForm(data={
            'room': self.other_room.pk,
            'user': self.user.pk,
            'booking_date': date.today() - timedelta(days=1),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('booking_date', form.errors)

    def test_booking_form_rejects_conflict_but_allows_current_record(self):
        conflict = BookingForm(data={
            'room': self.room.pk,
            'user': self.user.pk,
            'booking_date': self.booking_date,
        })
        self.assertFalse(conflict.is_valid())
        self.assertIn('Это помещение уже занято', str(conflict.non_field_errors()))

        edit = BookingForm(
            data={
                'room': self.room.pk,
                'user': self.user.pk,
                'booking_date': self.booking_date,
            },
            instance=self.booking,
        )
        self.assertTrue(edit.is_valid(), edit.errors)

    def test_create_edit_and_cancel_use_post(self):
        create_url = reverse('bookings:create')
        self.assertEqual(self.client.get(create_url).status_code, 200)
        response = self.client.post(create_url, {
            'room': self.other_room.pk,
            'user': self.user.pk,
            'booking_date': (date.today() + timedelta(days=7)).isoformat(),
        })
        self.assertEqual(response.status_code, 302)
        created = Booking.objects.get(room=self.other_room)

        edit_url = reverse('bookings:edit', args=(created.pk,))
        self.assertEqual(self.client.get(edit_url).status_code, 200)
        response = self.client.post(edit_url, {
            'room': self.other_room.pk,
            'user': self.user.pk,
            'booking_date': (date.today() + timedelta(days=8)).isoformat(),
        })
        self.assertEqual(response.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.booking_date, date.today() + timedelta(days=8))

        cancel_url = reverse('bookings:cancel', args=(created.pk,))
        csrf_client = Client(enforce_csrf_checks=True)
        detail_response = csrf_client.get(created.get_absolute_url())
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(csrf_client.get(cancel_url).status_code, 405)
        self.assertEqual(csrf_client.post(cancel_url).status_code, 403)
        csrf_token = csrf_client.cookies['csrftoken'].value
        self.assertEqual(
            csrf_client.post(
                cancel_url, HTTP_X_CSRFTOKEN=csrf_token
            ).status_code,
            302,
        )
        created.refresh_from_db()
        self.assertEqual(created.status, Booking.Status.CANCELLED)

    def test_list_filters_related_fields_and_statistics(self):
        response = self.client.get(reverse('bookings:bookings'), {
            'search': 'Тестовая', 'status': Booking.Status.ACTIVE,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['bookings'].object_list), [self.booking])
        self.assertEqual(
            self.client.get(reverse('bookings:statistics')).status_code, 200
        )
