from django.contrib import admin

# Register your models here.
from .models import ChatHistory,Event

admin.site.register(ChatHistory)
admin.site.register(Event)
