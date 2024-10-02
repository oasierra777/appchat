from django.urls import path

from apps.chat.views import home
from apps.chat.views import room

urlpatterns = [
    path('', home, name='home',),
    path('room/<int:room_id>/', room, name='room',),
]