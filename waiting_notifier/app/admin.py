from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['user_id', 'display_name', 'created_at']
    readonly_fields = ('user_id', 'display_name', 'created_at')


admin.site.register(User, UserAdmin)
