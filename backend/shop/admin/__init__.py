from django.contrib import admin
from shop.models import *
from .product_admin import ProductAdmin
from .product_image_admin import ProductImageAdmin
from .order_admin import OrderAdmin
from .cart_admin import CartAdmin
from .favorites_admin import FavoriteAdmin
from .subcategory_admin import SubCategoryAdmin


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Variants)
