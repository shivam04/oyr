from rest_framework.serializers import ModelSerializer

from .models import Order, ItemOrder
from account.serializers import UserDetailSerializer

from shop.serializers import ShopCreateUpdateSerializer

from items.serializers import ItemCreateUpdateSerializer


class OrderCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pickup_time',
            'order_number',
            'status'
        ]


class ShopOwnerOrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pickup_time',
            'order_number'
        ]


class OrderListSerializer(ModelSerializer):
    shop = ShopCreateUpdateSerializer(read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'shop',
            'user',
            'order_number',
        ]


class OrderDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    shop = ShopCreateUpdateSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'user',
            'shop',
            'pickup_time',
            'order_number',
        ]


class ItemOrderCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = [
            'item',
            'quantity',
            'order'
        ]


class ItemOrderListSerializer(ModelSerializer):
    order = OrderListSerializer(read_only=True)
    item = ItemCreateUpdateSerializer(read_only=True)

    class Meta:
        model = ItemOrder
        fields = [
            'item',
            'quantity',
            'order'
        ]
