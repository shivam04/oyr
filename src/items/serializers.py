from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Item
from shop.serializers import ShopCreateUpdateSerializer


class ItemCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'name',
            'stock',
            'cost',
            'shop',
            'slug'
        ]


class ItemDetailSerializer(ModelSerializer):
    shop_detail = SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'name',
            'stock',
            'cost',
            'shop_detail',
            'slug'
        ]

    def get_shop_detail(self, obj):
        return ShopCreateUpdateSerializer(obj.shop_detail(), many=True).data
