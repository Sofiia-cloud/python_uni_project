from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from rooms.models import Room
from .models import Booking


class BookingFilterForm(forms.Form):
    search = forms.CharField(
        label='Поиск', required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Помещение или пользователь',
        }),
    )
    booking_date = forms.DateField(
        label='Дата', required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    room = forms.ModelChoiceField(
        label='Помещение', queryset=Room.objects.all(), required=False,
        empty_label='Любое помещение',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        label='Статус', required=False,
        choices=(('', 'Любой статус'), *Booking.Status.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'booking_date' not in self.initial:
            self.initial['booking_date'] = date.today()

    class Meta:
        model = Booking
        fields = ('room', 'user', 'booking_date')
        labels = {
            'room': 'Помещение',
            'user': 'Пользователь',
            'booking_date': 'Дата бронирования',
        }
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'booking_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if not self.instance.pk and booking_date < date.today():
            raise ValidationError('Нельзя бронировать помещение на прошедшую дату.')
        return booking_date

    def clean(self):
        cleaned = super().clean()
        room = cleaned.get('room')
        booking_date = cleaned.get('booking_date')
        if not room or not booking_date:
            return cleaned
        conflicts = Booking.objects.active().filter(
            room=room, booking_date=booking_date,
        )
        if self.instance.pk:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if conflicts.exists():
            raise ValidationError(
                'Это помещение уже занято на выбранную дату.'
            )
        return cleaned
