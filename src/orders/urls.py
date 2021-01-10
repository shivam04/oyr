from .views import (
    OrderCreateAPIView,
    OrderUpdateApiView,
    OrderDetailApiView,
    OrderDeleteApiView,
    OrderListApiView,
    ShopOwnerUpdateApiView,
    ShopOwnerOrderListApiView,
    ShopOwnerDeleteApiView,
    ItemOrderCreateAPIView,
    ItemOrderDetailAPIView,
    ItemOrderListAPIView,
)
from django.urls import path

urlpatterns = [
    path('order-create/', OrderCreateAPIView.as_view(), name="order-create"),
    path('order-list/', OrderListApiView.as_view(), name="order-list"),
    path('shop-order-list/', ShopOwnerOrderListApiView.as_view(), name="shop-order-list"),
    path('item-order-create/', ItemOrderCreateAPIView.as_view(), name="item-order-create"),
    path('shop/<str:order_number>/edit/', ShopOwnerUpdateApiView.as_view(), name="shop-order-update"),
    path('shop/<str:order_number>/delete/', ShopOwnerDeleteApiView.as_view(), name="shop-order-delete"),
    path('<str:order_number>/', OrderDetailApiView.as_view(), name="order-detail"),
    path('<str:order_number>/edit/', OrderUpdateApiView.as_view(), name="order-update"),
    path('<str:order_number>/delete/', OrderDeleteApiView.as_view(), name="order-delete"),

    path('shop/<str:order_number>/item-order-list/', ItemOrderListAPIView.as_view(), name="item-order-list"),
    path('item/<int:id>/', ItemOrderDetailAPIView.as_view(), name="item-order-detail"),
]
