from datetime import date, timedelta
from io import BytesIO
from tempfile import TemporaryDirectory
from urllib.parse import quote

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from PIL import Image

from .forms import RoomForm
from bookings.models import Booking, User
from .models import Room


class RoomORMViewsTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='Большой зал', capacity=40)
        self.user = User.objects.create(name='Пользователь', email='room@example.com')

    def test_room_form_requires_positive_capacity(self):
        form = RoomForm(data={'name': 'Нулевой зал', 'capacity': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('capacity', form.errors)

    def test_slug_url_and_legacy_id_url(self):
        self.assertEqual(
            self.room.get_absolute_url(), f'/rooms/{quote(self.room.slug)}/'
        )
        self.assertEqual(self.client.get(self.room.get_absolute_url()).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('rooms:detail_by_id', args=(self.room.pk,))).status_code,
            200,
        )

    def test_available_rooms_respect_active_booking_status(self):
        target_date = date.today() + timedelta(days=2)
        Booking.objects.create(
            room=self.room, user=self.user, booking_date=target_date,
        )
        response = self.client.get(
            reverse('rooms:available'), {'date': target_date.isoformat()}
        )
        self.assertNotIn(self.room, response.context['rooms'])
        Booking.objects.update(status=Booking.Status.CANCELLED)
        response = self.client.get(
            reverse('rooms:available'), {'date': target_date.isoformat()}
        )
        self.assertIn(self.room, response.context['rooms'])

    def test_room_photo_upload_is_saved_and_displayed(self):
        image_file = BytesIO()
        Image.new('RGB', (2, 2), color='red').save(image_file, format='PNG')
        image_file.seek(0)
        upload = SimpleUploadedFile(
            'room.png', image_file.read(), content_type='image/png'
        )
        with TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                response = self.client.post(reverse('rooms:create'), {
                    'name': 'Фотостудия', 'capacity': 14, 'image': upload,
                })
                self.assertEqual(response.status_code, 302)
                room = Room.objects.get(name='Фотостудия')
                self.assertTrue(room.image.name.startswith('rooms/'))
                self.assertTrue(room.image.storage.exists(room.image.name))
                page = self.client.get(room.get_absolute_url())
                self.assertContains(page, room.image.url)
