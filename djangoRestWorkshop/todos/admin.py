from django.contrib import admin

from djangoRestWorkshop.todos.models import Todo, Category


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'username', 'is_done')

    def username(self, obj):
        return obj.user.username


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
