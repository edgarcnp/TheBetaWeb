from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def room(request, room):
    return HttpResponse(f"You're looking at room {room}.")
