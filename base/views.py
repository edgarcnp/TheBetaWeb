from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm, UserForm
from .models import Message, Room, Topic

# Create your views here.


def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)

        except User.DoesNotExist:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username OR password is incorrect")

    respond = {"page": page}
    return render(request, "base/login_register.html", respond)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_page(request):
    page = "register"
    form = UserCreationForm()

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get("username").lower()
            user.save()
            messages.success(request, "Account was created for " + user.username)
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "An error has occurred during registration")

    respond = {"page": page, "form": form}
    return render(request, "base/login_register.html", respond)


def home(request):
    query = request.GET.get("q") if request.GET.get("q") else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query)
        | Q(name__icontains=query)
        | Q(description__icontains=query)
    )
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))

    respond = {"rooms": rooms, "topics": topics, "messages": room_messages}
    return render(request, "base/home.html", respond)


def room(request, room_id):
    get_room = Room.objects.get(id=room_id)
    user_messages = get_room.message_set.all().order_by("-created")
    participants = get_room.participants.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to do that!")

        message = request.POST.get("body")
        if message:
            Message.objects.create(user=request.user, room=get_room, body=message)
            get_room.participants.add(request.user)
            return redirect("room", room_id=room_id)

    respond = {
        "rooms": get_room,
        "messages": user_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", respond)


def user_profile(request, user_id):
    get_user = User.objects.get(id=user_id)
    user_rooms = get_user.room_set.all()
    user_messages = get_user.message_set.all()
    user_topics = Topic.objects.all()

    respond = {
        "user": get_user,
        "rooms": user_rooms,
        "messages": user_messages,
        "topics": user_topics,
    }
    return render(request, "base/profile.html", respond)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    respond = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", respond)


@login_required(login_url="login")
def update_room(request, room_id):
    room_update = Room.objects.get(id=room_id)
    form = RoomForm(instance=room_update)

    if request.user != room_update.host:
        return HttpResponse("You are not allowed to do that!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room_update.name = request.POST.get("name")
        room_update.description = request.POST.get("description")
        room_update.topic = topic
        room_update.save()

        return redirect("home")

    respond = {"form": form, "room": room_update}
    return render(request, "base/room_form.html", respond)


@login_required(login_url="login")
def delete_obj(request, obj_type, obj_id):
    if obj_type == "room":
        obj_delete = Room.objects.get(id=obj_id)
        if request.user != obj_delete.host:
            return HttpResponse("You are not allowed to do that!")
    elif obj_type == "message":
        obj_delete = Message.objects.get(id=obj_id)
        if request.user != obj_delete.user:
            return HttpResponse("You are not allowed to do that!")
    else:
        return HttpResponse("Invalid object type!")

    if request.method == "POST":
        obj_delete.delete()
        return redirect("home")

    respond = {"obj": obj_delete, "obj_type": obj_type}
    return render(request, "base/delete.html", respond)


@login_required(login_url="login")
def update_user(request):
    user_update = request.user
    form = UserForm(instance=user_update)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user_update)
        if form.is_valid():
            user_update = form.save(commit=False)
            user_update.username = form.cleaned_data.get("username").lower()
            user_update.save()
            return redirect("user-profile", user_id=user_update.id)

    respond = {"form": form}
    return render(request, "base/update-user.html", respond)
