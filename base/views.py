from django.shortcuts import redirect, render

from .forms import RoomForm
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


def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    respond = {"form": form}
    return render(request, "base/room_form.html", respond)


def update_room(request, room_id):
    room_update = Room.objects.get(id=room_id)
    form = RoomForm(instance=room_update)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room_update)
        if form.is_valid():
            form.save()
            return redirect("home")

    respond = {"form": form}
    return render(request, "base/room_form.html", respond)
