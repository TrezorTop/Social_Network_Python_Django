from django.contrib import admin
from .models import File, Category


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_file', 'updated_at', 'created_at', 'author')
    search_fields = ('title',)
    list_filter = ('author',)
    ordering = ('-created_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'updated_at', 'created_at',)
    search_fields = ('title',)
    list_filter = ('profile',)
    ordering = ('title',)


admin.site.register(File, FileAdmin)
admin.site.register(Category, CategoryAdmin)
