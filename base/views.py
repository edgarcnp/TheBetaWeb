from django.shortcuts import redirect, render
from django.db.models import Q

from .forms import RoomForm
from .models import Room, Topic

# Create your views here.


def home(request):
    query = request.GET.get("q") if request.GET.get("q") else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    topics = Topic.objects.all()

    respond = {"rooms": rooms, "topics": topics}
    return render(request, "base/home.html", respond)


def room(request, room_id):
    rooms = Room.objects.get(id=room_id)
    respond = {"rooms": rooms}
    return render(request, "base/room.html", respond)


def create_room(request):
    form = None
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


def delete_room(request, room_id):
    room_delete = Room.objects.get(id=room_id)
    if request.method == "POST":
        room_delete.delete()
        return redirect("home")

    respond = {"item": room_delete}
    return render(request, "base/delete.html", respond)
