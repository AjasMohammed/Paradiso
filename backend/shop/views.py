from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.core.files import File
from io import BytesIO

from math import ceil
import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


class ProductsView(APIView):

    def get(self, request, format=None):
        products = Product.objects.all().order_by('category__name')
        serializer = ProductSerializer(products, many=True)
        data = serializer.data

        ordered_products = {}
        for item in data:
            category_name = item['category']['name']
            if category_name not in ordered_products.keys():
                ordered_products[category_name] = []
            ordered_products[category_name].append(item)

        products_dict = {}
        for category, items in ordered_products.items():
            rows = ceil(len(items)/5)
            n = 0
            product_row = []

            for i in range(rows):
                prod = items[n:n+5]
                n += 5
                product_row.append(prod)
            if category not in products_dict.keys():
                products_dict[category] = []
            products_dict[category].append(product_row)
              
        return Response(products_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_view(request, id):
    product = Product.objects.get(id = id)
    
    serializer = ProductSerializer(product)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def like_product(request, id):
    product = Product.objects.get(id = id)
    product.likes += 1
    product.save()

    return Response({'message': 'Liked Product'})


@login_required
@api_view(['POST'])
def add_to_cart(request, id):

    product = get_object_or_404(Product, pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # cart_item.quantity += 1
    cart_item.save()

    return Response({'message': 'Product Added'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    cart.products.remove(product)

    return Response({'message': 'Removed from Cart'})


@api_view(['GET'])
def get_cart_items(request, is_count):
    try:
        cart  = Cart.objects.prefetch_related('cartitem_set').get(user=request.user)
        items = cart.cartitem_set.all()
        if is_count == 'true':
            item_no = items.count()
            return Response({'count':item_no})
        elif is_count == 'false':
            serializer = CartItemSerializer(items, many=True)
        
        return Response(serializer.data)
    except :
        return Response({'message': 'Cart is Empty'})


@api_view(['GET'])
def check_in_cart(request, id):
    cart = get_object_or_404(Cart, user=request.user)
    try:
        cart_items = get_object_or_404(CartItem, cart=cart, product_id = id)
        return Response(True)
    except:
        return Response(False)

@login_required
@api_view(['GET'])
def view_favorite(request):
    user = request.user
    favorite = Favorite.objects.get(user=user)
    prod_id = request.query_params.get('id')
    print(prod_id)

    if prod_id:
        try:
            product = favorite.products.get(id=prod_id)
            print('done')
            return Response(True)
        except Exception as e:
            return Response(False)

    else:
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)



@login_required
@api_view(['POST'])
def add_to_favorite(request, id):
    product = Product.objects.get(id=id)
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite.products.add(product)

    return Response({'message': 'Add to Favorite Successfully'}, status=status.HTTP_200_OK)


@login_required
@api_view(['POST'])
def remove_from_favorite(request, id):
    product = Product.objects.get(id=id)
    try:
        favorite = get_object_or_404(Favorite, user=request.user)
        favorite.products.remove(product)
    except:
        print('Not Found')

    return Response({'message': 'Removed from Favorite Successfully'}, status=status.HTTP_200_OK)





def addProd():
    
    url = "https://fakestoreapi.com/products"

    response = requests.get(url)
    items = response.json()

    for item in items:
        id = item['id']
        title = item['title']
        price = item['price']
        category = item['category']
        description = item['description']
        image_url = item['image']
        # rating = item['rating']['rate']
        likes = item['rating']['count']
        tags = category.split(' ')

        category, _ = Category.objects.get_or_create(name=category)
        prod = Product(name=title, price=price, category=category, description=description, likes=likes)
        prod.save()

        for tag in tags:
            tag, _ = Tag.objects.get_or_create(name=tag)
            prod.tags.add(tag)
        


        # Fetch the image from the URL and save it to the media folder
        img_content = requests.get(image_url).content
        # Create a BytesIO object from the image content
        img_bytes_io = BytesIO(img_content)
        prod_image = ProductImage(product=prod)
        prod_image.image.save(f"{id}.jpg", File(img_bytes_io))


        print(f'Produt: {id} added......')
