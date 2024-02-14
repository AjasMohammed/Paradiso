from django.urls import path
from .views import *


urlpatterns = [
    path('products/', ProductsView.as_view(), name='products_view'),
    path('product-category/', CategoryProducts.as_view(), name='product_category'),
    path('product-subcategory/<str:name>/', GetSubCategories.as_view(), name='product_subcategory'),
    path('related-products/', RelatedProducts.as_view(), name='related_product'),
    path('product/<int:id>/', SingleProductView.as_view(), name='product_view'),
    path('like-product/<int:id>/', LikeProductView.as_view(), name='like_product'),
    path('add-to-cart/<int:id>/', AddToCart.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('check-in-cart/<int:id>/', Check_In_Cart.as_view(), name='check_in_cart'),
    path('increment-quantity/<int:id>/', IncrementQuantity.as_view(), name='increment_quantity'),
    path('decrement-quantity/<int:id>/', DecrementQuantity.as_view(), name='decrement_quantity'),
    path('get-cart-items/<str:is_count>/', GetCartItems.as_view(), name='get_cart_items'),
    path('favorite/', ViewFavorite.as_view(), name='favorite'),
    path('favorite/<int:id>/', ViewFavorite.as_view(), name='favorite'),
    path('place-order/', PlaceOrder.as_view(), name='place_order'),
    path('search-query/', SearchQuery.as_view(), name='search_query'),
]
