from django.db import models
from django.db.models import Case, Value, When
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Room(models.Model):
    name = models.CharField('Название', max_length=120, unique=True)
    slug = models.SlugField('Адрес', max_length=140, unique=True, blank=True)
    capacity = models.PositiveIntegerField(
        'Вместимость', validators=[MinValueValidator(1)]
    )
    capacity_category = models.GeneratedField(
        expression=Case(
            When(capacity__gte=30, then=Value('Большое')),
            default=Value('Стандартное'),
            output_field=models.CharField(max_length=20),
        ),
        output_field=models.CharField('Категория вместимости', max_length=20),
        db_persist=True,
        verbose_name='Категория вместимости',
    )
    image = models.ImageField(
        'Изображение', upload_to='rooms/', blank=True, null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'помещение'
        verbose_name_plural = 'помещения'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or 'room'
            candidate = base
            suffix = 2
            while Room.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f'{base}-{suffix}'
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('rooms:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name} ({self.capacity} мест)'
