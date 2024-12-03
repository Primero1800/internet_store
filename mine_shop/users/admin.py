from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'password', 'is_active', 'is_superuser', 'is_staff')
    list_display_links = ('email', 'username', )
    search_fields = ('email', 'username',)
    list_per_page = 30

admin.site.register(User, UserAdmin)
