from django.contrib import admin
import main.models as models

class ProjectInline(admin.TabularInline):
    model = models.Project.users.through
    extra = 1

class DoneInline(admin.TabularInline):
    model = models.Done.user.through
    extra = 1

class EntranceInline(admin.TabularInline):
    model = models.Entrance.user.through
    extra = 1

class UserAdmin(admin.ModelAdmin):
    list_display = (['username', 'date_joined'])
    inlines = [ProjectInline, DoneInline, EntranceInline]
    filter_horizontal = (['projects'])
    readonly_fields = (['date_joined'])
    search_fields = ['username']
admin.site.register(models.User, UserAdmin)

class UserInline(admin.TabularInline):
    model = models.Project.users.through
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = (['name', 'user_f', 'user_count'])

    def user_f(self, project):
        return ', '.join(project.users.values_list('username', flat=True))
    user_f.short_description = 'users'

    # inlines = [UserInline]

    @admin.display(description='Number of Users')
    def user_count(self, obj):
        return obj.users.count()

    search_fields = ['name']
admin.site.register(models.Project, ProjectAdmin)

class TaskInline(admin.TabularInline):
    model = models.Transaction.task.through
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = (['name', 'project_f'])
    inlines = [TaskInline]

    def project_f(self, task):
        return task.project.name
    project_f.short_description = 'project'

admin.site.register(models.Task, TaskAdmin)


class TransactionProjectInline(admin.TabularInline):
    model = models.Transaction.project.through
    extra = 1

class TransactionTaskInline(admin.TabularInline):
    model = models.Transaction.task.through
    extra = 1

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('project_f', 'task_f', 'action', 'time')


    def project_f(self, project):
        return ', '.join(project.project.values_list('name', flat=True))
    project_f.short_description = 'project'

    def task_f(self, task):
        return ', '.join(task.task.values_list('name', flat=True))
    task_f.short_description = 'task'

    list_filter = (['action'])
    inlines = [TransactionProjectInline, TransactionTaskInline]
    list_display_links = ['project_f']
    search_fields = ['action']
admin.site.register(models.Transaction, TransactionAdmin)

class DoneUserInline(admin.TabularInline):
    model = models.Done.user.through
    extra = 1

class DoneAdmin(admin.ModelAdmin):
    list_display = (['user_f', 'name'])
    search_fields = ['name']
    inlines = [DoneUserInline]

    def user_f(self, project):
        return ', '.join(project.user.values_list('username', flat=True))
    user_f.short_description = 'user'
admin.site.register(models.Done, DoneAdmin)

class EntranceUserInline(admin.TabularInline):
    model = models.Entrance.user.through
    extra = 1

class EntranceAdmin(admin.ModelAdmin):
    list_display = (['user_f', 'time'])
    inlines = [EntranceUserInline]

    def user_f(self, project):
        return ', '.join(project.user.values_list('username', flat=True))
    user_f.short_description = 'user'
admin.site.register(models.Entrance, EntranceAdmin)
