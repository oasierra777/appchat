from django.contrib import admin
from apps.chat.models import Message
from apps.chat.models import Room

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'timestamp')
    list_filter = ('room', 'user')

admin.site.register(Message, MessageAdmin)
admin.site.register(Room)
