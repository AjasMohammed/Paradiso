from django.contrib import admin
from shop.models import Favorite


class FavoriteItemsInline(admin.TabularInline):
    model = Favorite.products.through
    extra = 1


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']

    inlines = [FavoriteItemsInline]