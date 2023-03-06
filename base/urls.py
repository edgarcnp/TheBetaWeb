from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:room>", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:room_id>", views.update_room, name="update-room"),
]
