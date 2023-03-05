from django.contrib import admin

from .models import Message, Room, Topic

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
