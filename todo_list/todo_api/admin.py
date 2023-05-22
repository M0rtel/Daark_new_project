from django.contrib import admin

from .models import List, Task, Folder

admin.site.register(Folder)
admin.site.register(List)
admin.site.register(Task)
