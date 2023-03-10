from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_route),
    path("rooms", views.get_rooms),
    path("rooms/<str:room_id>", views.get_room),
]
