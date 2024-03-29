from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')
    readonly_fields = ('password',)
    

admin.site.register(CustomUser, UserAdmin)