from django.contrib import admin

# Register your models here.
from .models import ChatHistory,Event

admin.site.register(ChatHistory)


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Event, EventAdmin)
