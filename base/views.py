from django.shortcuts import render

from .models import Room

# Create your views here.


def home(request):
    rooms = Room.objects.all()
    respond = {"rooms": rooms}
    return render(request, "base/home.html", respond)


def room(request, room_id):
    rooms = Room.objects.get(id=room_id)
    respond = {"rooms": rooms}
    return render(request, "base/room.html", respond)
