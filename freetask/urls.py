from django.urls import path
from main.views import landing, tasks, get_tasks, add_task, update_task, delete_task
from django.contrib import admin

urlpatterns = [
    path('', landing),
    path('tasks', tasks),
    path('admin/', admin.site.urls),
    path('get-tasks', get_tasks),
    path('add-task', add_task),
    path('update-task', update_task),
    path('delete-task', delete_task),
]