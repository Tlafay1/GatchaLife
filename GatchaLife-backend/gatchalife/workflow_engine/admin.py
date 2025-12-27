from django.contrib import admin
from .models import AsyncJob

@admin.register(AsyncJob)
class AsyncJobAdmin(admin.ModelAdmin):
    list_display = ("id", "job_type", "status", "created_at", "updated_at")
    list_filter = ("job_type", "status")
    search_fields = ("id", "error_message")
    readonly_fields = ("created_at", "updated_at", "payload", "result")