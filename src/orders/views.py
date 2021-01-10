from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from .models import Order, ItemOrder
from .permissions import IsOwnerOrReadOnly, IsShopOwner, IsOrderOwner
from .serializers import OrderCreateUpdateSerializer, OrderListSerializer, OrderDetailSerializer, \
    ShopOwnerOrderUpdateSerializer, ItemOrderCreateUpdateSerializer, ItemOrderListSerializer
from shop.models import Shop

from items.models import Item


class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    querySet = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def perform_create(self, serializer):
        shop = self.request.data.get('shop')
        shopDetail = Shop.objects.filter(id=shop).first()
        serializer.save(user=self.request.user, shop=shopDetail)


class OrderListApiView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        querySet = Order.objects.filter(user=self.request.user)
        return querySet


class OrderDetailApiView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'order_number'


class OrderUpdateApiView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer
    lookup_field = 'order_number'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        shop = self.request.data.get('shop')
        shopDetail = Shop.objects.filter(id=shop).first()
        serializer.save(user=self.request.user, shop=shopDetail)


class OrderDeleteApiView(DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_number'

    def perform_destroy(self, instance):
        items = ItemOrder.objects.filter(order__order_number=instance.order_number)
        mp = {}
        for item in items:
            if item.item.id not in mp:
                mp[item.item.id] = 0
            mp[item.item.id] += int(item.quantity)
        for k, v in mp.items():
            item = Item.objects.filter(id=k).first()
            if item is not None:
                item.stock += int(v)
                item.save()
        instance.delete()


class ShopOwnerUpdateApiView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    lookup_field = 'order_number'
    permission_classes = [IsAuthenticated, IsShopOwner]
    serializer_class = ShopOwnerOrderUpdateSerializer


class ShopOwnerOrderListApiView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        querySet = Order.objects.filter(shop__user=self.request.user)
        return querySet


class ShopOwnerDeleteApiView(DestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = 'order_number'
    permission_classes = [IsAuthenticated, IsShopOwner]
    serializer_class = ShopOwnerOrderUpdateSerializer


class ItemOrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    querySet = ItemOrder.objects.all()
    serializer_class = ItemOrderCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.get("items") if 'items' in self.request.data else self.request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, data, many)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, data, many):
        serializer.save()
        items = []
        if many:
            items = items + data
        else:
            items.append(data)

        for item in items:
            itemDetail = Item.objects.filter(id=item['item']).first()
            itemDetail.stock = itemDetail.stock - int(item['quantity'])
            itemDetail.save()


class ItemOrderDetailAPIView(RetrieveAPIView):
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrderOwner]


class ItemOrderListAPIView(ListAPIView):
    serializer_class = ItemOrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        order_number = self.kwargs.get('order_number')
        querySet = ItemOrder.objects.filter(order__order_number__icontains=order_number)
        return querySet
