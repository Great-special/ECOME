from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

import stripe
from Customer.models import Customer

from .models import Category, Product, Order, OrderItem, ShippingAddress
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, MyOrderSerializer
# Create your views here.

# using apiview gives you access to control and over ride methods, just like working with function base view
class ProductListView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all() # getting the list of product from the database
        serializer = ProductSerializer(products, many=True) # converting to a serialized data
        return Response(serializer.data)

class ProductLatestView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:7] # getting the list of product from the database
        serializer = ProductSerializer(products, many=True) # converting to a serialized data
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug) # getting a single product from the database
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug) # getting a single product from the database
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)



class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products':[]})    
    

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    datas = request.data
    print(datas)
    serializer = OrderSerializer(data=request.data)
    # print(serializer)
    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # for item in serializer.validated_data['items']:
            
        #     print(item.get('quantity'), 'quantity')
        #     print(item.get('product').price, 'price')
            
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        

        try:
            charge = stripe.Charge.create(
                amount = int(paid_amount * 100),
                currency = 'USD',
                description='Charge form Ecome',
                source = serializer.validated_data['stripe_token']
            )
            print(serializer.validated_data['stripe_token'], paid_amount)
            
            serializer.save(user=request.user, paid_amount=paid_amount)
        except Exception:
            print('An error occurred')
            return Response(serializer.errors)
        else:
            print('No error occurred')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

