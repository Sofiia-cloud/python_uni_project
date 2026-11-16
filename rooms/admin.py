

from django.contrib import admin
from django.db.models import Count

from bookings.models import Booking
from .models import Room


class RoomBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    show_change_link = True
    fields = ('user', 'booking_date', 'status')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'capacity_category', 'slug', 'booking_count')
    list_filter = ('capacity',)
    search_fields = ('name', 'slug')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('booking_count',)
    inlines = (RoomBookingInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            booking_count_value=Count('bookings')
        )

    @admin.display(description='Бронирований')
    def booking_count(self, obj):
        return obj.booking_count_value
