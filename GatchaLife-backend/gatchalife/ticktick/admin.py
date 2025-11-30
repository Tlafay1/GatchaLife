from django.contrib import admin
from .models import ProcessedTask, TickTickTask, TickTickColumn, TickTickProject

admin.site.register(ProcessedTask)
admin.site.register(TickTickTask)
admin.site.register(TickTickColumn)
admin.site.register(TickTickProject)