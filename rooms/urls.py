from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.rooms, name='list'),
    path('available/', views.available, name='available'),
    path('new/', views.room_create, name='create'),
    path('<int:room_id>/', views.room_detail_by_id, name='detail_by_id'),
    path('<str:slug>/edit/', views.room_edit, name='edit'),
    path('<str:slug>/', views.room_detail, name='detail'),
]
