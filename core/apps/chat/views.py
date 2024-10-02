from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from apps.chat.models import Room

def home(request):
    rooms = Room.objects.all()
    return render(request, 'chat/home.html', {'rooms':rooms})

@login_required
def room(request, room_id):
    try:
        room = request.user.room_joined.get(id=room_id)
    except Room.DoesNotExist:
        error_message = 'No tiene permisos de accesoa aeste chat'
        return render(request, 'chat/home.html', {
            'error_message':error_message,
            'rooms':Room.objects.all()
            })
    return render(request, 'chat/room.html', {'room':room})
        