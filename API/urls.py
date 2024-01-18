from django.urls import path 
from . import views
urlpatterns = [
    path('menu-items/',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.MenuItemObject.as_view()),
    path('category/',views.CategoryView.as_view()),
    path('category/<int:pk>',views.CateogryObject.as_view()),

    # user role managemeng 
    path("group/manager/users",views.UserManageView.as_view()),
    path("group/manager/user/<int:pk>",views.UserManageView.as_view()),
    path("group/delivery_crew/users",views.DeliveryCrewManageView.as_view()),
    path("group/delivery_crew/user/<int:pk>",views.DeliveryCrewManageView.as_view()),
    # todo take data via serilizer and validate  
    path("cart/menu-items",views.CartMenuItemsView.as_view()),
    path("cart/menu-items/<int:pk>",views.CartMenuItemsView.as_view()),

    # todo : 
    path("orders",views.OrderView.as_view({'get':'get','post':'post'})),
    path("orders/<int:pk>",views.OrderView.as_view({'get':'get_orderid'})),
]