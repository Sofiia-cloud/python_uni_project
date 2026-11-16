from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.bookings, name='bookings'),
    path('statistics/', views.statistics, name='statistics'),
    path('new/', views.booking_create, name='create'),
    path('<int:booking_id>/edit/', views.booking_edit, name='edit'),
    path('<int:booking_id>/cancel/', views.booking_cancel, name='cancel'),
    path('<int:booking_id>/', views.booking_detail, name='detail'),
]
