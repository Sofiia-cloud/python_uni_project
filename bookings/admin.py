

from django.contrib import admin
from django.db.models import Count

from .models import Booking, User


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    show_change_link = True
    fields = ('room', 'booking_date', 'status')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'booking_count')
    search_fields = ('name', 'email')
    inlines = (BookingInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            booking_count_value=Count('bookings')
        )

    @admin.display(description='Бронирований')
    def booking_count(self, obj):
        return obj.booking_count_value


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'room')
    search_fields = ('room__name', 'user__name', 'user__email')
    date_hierarchy = 'booking_date'
    list_select_related = ('room', 'user')
    ordering = ('-booking_date', '-id')
