from django.shortcuts import render

from .models import Room

# Create your views here.


def home(request):
    respond = {}
    return render(request, "base/home.html", respond)


def room(request, room_id):
    rooms = Room.objects.get(id=room_id)
    respond = {"room_name": rooms.name, "room_description": rooms.description}
    return render(request, "base/room.html", respond)
