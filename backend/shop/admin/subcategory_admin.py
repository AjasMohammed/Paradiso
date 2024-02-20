from django.contrib import admin
from shop.models import *


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

    search_fields = ['name__icontains']
