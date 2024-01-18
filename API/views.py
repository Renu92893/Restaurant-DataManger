from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import MenuItem ,Category , Cart , Order ,OrderItem 
from .serializers import MenuItemSerializer ,CategorySerializer , UserObjectSerializer , CartSerializer , OrderSerializer , OrderMenuItemSerializer 
from django.contrib.auth.models import User , Group
from rest_framework.response import Response
from rest_framework import status , viewsets
from django.db.models import Sum
'''
todo 
1. authentication and authorization implementation 
2. permissions policy update and implmentation 
3. serlialization of post data to show form in frontend 
4. limit user access via read only implement 
5. To implement right Response with appropriate status code 

'''
# menu-item endpoint | Open to all   # todo restriction is to be set 
# GET : ALL | POST : Only Manager 
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# GET : ALL | POST & PUT & DELETE : Only Manager
class MenuItemObject(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


#category class endpoint | Open to all  # todo restriction is to be set
# GET : ALL | POST : Only Manager 
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# GET : ALL | POST & PUT & DELETE : Only Manager
class CateogryObject(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



# user management view | Open to all   # todo restriction is to be set 
class UserManageView(APIView):
    # ALL 
    def get(self,request , format = None):
        # user_names = User.objects.all()
        # user_serializer = UserObjectSerializer(user_names , many = True )
        # return Response(user_serializer.data)
        manager_user = User.objects.filter(groups__name = "Manager")
        manager_user_serializer = UserObjectSerializer(manager_user ,many=True)
        return Response(manager_user_serializer.data)
    # Only Manager 
    def post(self,request , format = None):
        username = request.POST.get('username')
        if username :
            usr = get_object_or_404(User, username=username)
            manager = Group.objects.get(name = "Manager")
            manager.user_set.add(usr)
            return Response({'message':"ok"})
        return Response({'message':'error'}, status= status.HTTP_400_BAD_REQUEST)
    # Only Manager
    def delete(self,request,pk,format=None ):
        usr = get_object_or_404(User, id = pk)
        manager = Group.objects.get(name = "Manager")
        manager.user_set.remove(usr)
        return Response({'message':"ok removed "})
# class UserManagerDelete(APIView):
#     def delete(self,request,pk,format=None ):
#         usr = get_object_or_404(User, id = pk)
#         manager = Group.objects.get(name = "Manager")
#         manager.user_set.remove(usr)
#         return Response({'message':"ok removed "})

class DeliveryCrewManageView(APIView):
    # Manager and Delivery_Crew  
    def get(self,request,format = None):
        crew = User.objects.filter(groups__name = "Delivery_crew")
        crew_serializer = UserObjectSerializer(crew,many = True)
        return Response(crew_serializer.data)
    
    def post(self,request , format = None):
        username = request.POST.get('username')
        if username :
            usr = get_object_or_404(User, username=username)
            manager = Group.objects.get(name = "Delivery_crew")
            manager.user_set.add(usr)
            return Response({'message':"ok"})
        return Response({'message':'error'}, status= status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None ):
        usr = get_object_or_404(User, id = pk)
        manager = Group.objects.get(name = "Delivery_crew")
        manager.user_set.remove(usr)
        return Response({'message':"ok removed "})


class CartMenuItemsView(APIView):
    # customer all methods 
    def get(self,request,format = None):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user__id = request.user.id)
            cart_serialized = CartSerializer(cart,many=True)
            return Response(cart_serialized.data )
        return Response({"Message":"NO "})
    def post(self,request):
        if request.user.is_authenticated:
            menu = get_object_or_404(MenuItem , id = request.POST.get('menu_id'))
            quantity = request.POST.get("Quantity")
            cart = Cart.objects.create(user = request.user , menuitem = menu ,quantity = quantity,price = menu.price * int(quantity) , unit_price = menu.price  )
            return Response({"message":"OK"})
        return Response({"Meesage":"NO"})
    def delete(self,request,pk):
        if request.user.is_authenticated:
            item = get_object_or_404( Cart ,user__id = request.user.id,id = pk)
            item.delete()
            return Response({"Meesage":"OK"})
        return Response({"Meesage":"NO"})
        
## menu items is not showing correctly when featcing order vai endpoint on order no and order detain is showing 
class OrderView(viewsets.ViewSet):
    def get(self,request):
            order = Order.objects.filter(user__id = request.user.id)
            orders_serializer = OrderSerializer(order,many = True)
            return Response(orders_serializer.data)
    def post(self,request):
            cart = Cart.objects.filter(user = request.user)
            total_price  = cart.aggregate(Sum('price'))
            order = Order(user = request.user,total = total_price["price__sum"])
            order.save()
            objects =[]
            for item in cart:
                objects.append(OrderItem(order=order, menuitem=item.menuitem ,quantity=item.quantity , unit_price=item.unit_price,price=item.price))
            OrderItem.objects.bulk_create(objects)
            cart.delete()
            ordered_items = OrderItem.objects.filter(user__id = request.user)
            items_serialized = OrderMenuItemSerializer(ordered_items , many = True)
            return Response(items_serialized.data)
    def get_orderid(self,request,pk):
            order = get_object_or_404(Order ,pk=request.GET["order_id"])
            # ordered_items = OrderItem.objects.filter(order = request.user)
            items_serialized = OrderSerializer(order )
            return Response(items_serialized.data)   

class SingleOrderView(APIView):
        
    
