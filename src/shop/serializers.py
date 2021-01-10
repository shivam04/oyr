from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Shop
from account.serializers import UserDetailSerializer


class ShopCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'name',
            'lisence_number',
            'slug'
        ]


class ShopListSerializer(ModelSerializer):
    user_detail = SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'name',
            'lisence_number',
            'slug',
            'user_detail'
        ]

    def get_user_detail(self, obj):
        return UserDetailSerializer(obj.user_detail(), many=True).data
