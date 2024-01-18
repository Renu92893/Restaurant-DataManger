from rest_framework import serializers
from .models import MenuItem , Category , Cart , Order, OrderItem
from django.contrib.auth.models import User 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True )
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category_id','category']

class UserObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ["id","username","email"]
class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True )
    class Meta:
        model = Cart 
        fields = ['id','menuitem','quantity','unit_price','price']
class OrderMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["menuitem","quantity","unit_price","price"]
        depth = 1
class OrderSerializer(serializers.ModelSerializer):
    menuitem = OrderMenuItemSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ["id","status","total","date","delivery_crew"]

