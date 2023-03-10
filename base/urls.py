from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("activity/", views.activity_page, name="activity"),
    path("create-room/", views.create_room, name="create-room"),
    path("delete/<str:obj_type>/<str:obj_id>", views.delete_obj, name="delete"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/<str:user_id>", views.user_profile, name="user-profile"),
    path("register/", views.register_page, name="register"),
    path("room/<str:room_id>", views.room, name="room"),
    path("topics/", views.topic_page, name="topics"),
    path("update-room/<str:room_id>", views.update_room, name="update-room"),
    path("update-user/", views.update_user, name="update-user"),
]
