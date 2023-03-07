from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:room_id>", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("delete-room/<str:room_id>", views.delete_message, name="delete-room"),
    path("delete-message/<str:message_id>", views.delete_message, name="delete-message"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),
    path("update-room/<str:room_id>", views.update_room, name="update-room"),
]
