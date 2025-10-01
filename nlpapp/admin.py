from django.contrib import admin
from .models import Upload, UserSession, WordCloudHistory

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'created_at')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_name', 'started_at', 'finished_at')

@admin.register(WordCloudHistory)
class WordCloudHistoryAdmin(admin.ModelAdmin):
    list_display = ('upload', 'generated_at', 'image')
