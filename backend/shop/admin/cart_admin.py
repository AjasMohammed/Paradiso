from django.contrib import admin
from shop.models import CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_diplay = ['user']
    inlines = [CartItemInline]
