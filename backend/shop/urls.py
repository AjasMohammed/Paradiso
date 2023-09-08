from django.urls import path
from .views import *


urlpatterns = [
    path('products', ProductsView.as_view(), name='productsView'),
    path('product/<int:id>', product_view, name='product_view'),
    path('add-to-cart/<int:id>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>', remove_from_cart, name='remove-from-cart'),
    path('check-in-cart/<int:id>', check_in_cart, name='check-in-cart'),
    path('get-cart-items/<str:is_count>', get_cart_items, name='get-cart-items'),
    path('view-favorite', view_favorite, name='view-favorite'),
    path('add-to-favorite/<int:id>', add_to_favorite, name='add-to-favorite'),
    path('remove-from-favorite/<int:id>', remove_from_favorite, name='remove-from-favorite'),

]