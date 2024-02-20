from django.contrib import admin
from shop.models import OrderItem


class OrderItemsInline(admin.StackedInline):
    model = OrderItem
    fields = ('order', 'product', 'quantity')
    readonly_fields = ('product', 'quantity')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'is_paid', 'is_delivered', 'amount']
    list_filter = ['is_paid', 'is_delivered']
    # Specify the order of fields
    fields = ('user', 'payment_id', 'amount', 'address', 'phone')
    readonly_fields = ('user', 'payment_id', 'amount', 'address', 'phone')

    inlines = [OrderItemsInline]
