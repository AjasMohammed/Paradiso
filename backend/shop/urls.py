from django.urls import path
from .views import *


urlpatterns = [
    path('products/', ProductsView.as_view(), name='products_view'),
    path('product-category/', CategoryProducts.as_view(), name='product-category'),
    path('product-subcategory/<str:name>/', GetSubCategories.as_view(), name='product-subcategory'),
    path('related-products/', RelatedProducts.as_view(), name='related-product'),
    path('product/<int:id>/', SingleProductView.as_view(), name='product_view'),
    path('like-product/<int:id>/', LikeProductView.as_view(), name='like_product'),
    path('add-to-cart/<int:id>/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:id>/',
         RemoveFromCart.as_view(), name='remove-from-cart'),
    path('check-in-cart/<int:id>/', Check_In_Cart.as_view(), name='check-in-cart'),
    path('get-cart-items/<str:is_count>/',
         GetCartItems.as_view(), name='get-cart-items'),
    path('view-favorite', ViewFavorite.as_view(), name='view-favorite'),
    path('add-to-favorite/<int:id>/',
         ViewFavorite.as_view(), name='add-to-favorite'),
    path('remove-from-favorite/<int:id>/',
         RemoveFromFavorite.as_view(), name='remove-from-favorite'),
    path('place-order/', PlaceOrder.as_view(), name='place-order'),
    path('search-query/', SearchQuery.as_view(), name='search-query'),
    path('payment/', Payment.as_view(), name='payment'),
]
