from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.files import File
from io import BytesIO
import requests
import random
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from decouple import config
import stripe


class ProductsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

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

        return Response(ordered_products, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def category_products(request):
    name = request.query_params.get('category')
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def sample_images(requests):
    images = ProductImage.objects.all()
    if len(images) % 2 == 0:
        n = len(images)//2
    else:
        n = (len(images)+1) // 2
    random_images = random.choices(images, k=n)
    serializer = ProductImageSerializer(random_images, many=True)
    data = []
    for i in range(0, len(serializer.data), 2):
        data.append([serializer.data[i], serializer.data[i+1]])

    return Response(data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def product_view(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, id):
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()

    return Response({'message': 'Liked Product'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    # cart_item.quantity += 1
    cart_item.save()

    return Response({'message': 'Product Added'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    cart.products.remove(product)
    print(cart.update_total())

    return Response({'message': 'Removed from Cart'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request, is_count):
    try:
        cart = Cart.objects.prefetch_related(
            'cartitem_set').get(user=request.user)

        items = cart.cartitem_set.all()
        if is_count == 'true':
            item_no = items.count()
            return Response({'count': item_no})
        elif is_count == 'false':
            serializer = CartItemSerializer(items, many=True)

            context = {
                'data': serializer.data,
                'total': cart.total
            }

        return Response(context, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Cart is Empty'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_in_cart(request, id):
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = get_object_or_404(CartItem, cart=cart, product_id=id)
        return Response(True)
    except:
        return Response(False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_favorite(request):
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user)
    except Exception as e:
        return Response(False)
    prod_id = request.query_params.get('id')

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorite(request, id):
    product = Product.objects.get(id=id)
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite.products.add(product)

    return Response({'message': 'Add to Favorite Successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_favorite(request, id):
    product = Product.objects.get(id=id)
    try:
        favorite = get_object_or_404(Favorite, user=request.user)
        favorite.products.remove(product)
    except:
        print('Not Found')

    return Response({'message': 'Removed from Favorite Successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    data = request.data
    data['user'] = user.pk

    order_items = data.pop('products', [])
    order_items_ids = [id['product'] for id in order_items]
    products = Product.objects.filter(id__in=order_items_ids)

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        order = serializer.save()

        for product in products:
            print(product)
            OrderItem.objects.create(order=order, product=product)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Order Placed Successfully.'}, status=status.HTTP_200_OK)


class SearchQuery(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get('query')
        print('name', Product.objects.filter(name__icontains=keyword))
        print('catagory', Product.objects.filter(
            category__name__icontains=keyword))
        print('tags', Product.objects.filter(tags__name__icontains=keyword))
        results = Product.objects.filter(Q(name__icontains=keyword) | Q(
            category__name__icontains=keyword) | Q(tags__name__icontains=keyword))
        print(results)
        if results:
            serializer = ProductSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def payment(request):
    stripe.api_key = config('STRIPE_KEY')
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='inr',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(data= test_payment_intent, status=status.HTTP_200_OK)

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
        prod = Product(name=title, price=price, category=category,
                       description=description, likes=likes)
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
