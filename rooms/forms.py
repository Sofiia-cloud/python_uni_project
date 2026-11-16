from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'capacity', 'image')
        labels = {
            'name': 'Название помещения',
            'capacity': 'Вместимость',
            'image': 'Фотография помещения',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
