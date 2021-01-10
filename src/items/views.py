from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Item
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView

from account.models import UserDetails

from .permissions import IsOwnerOrReadOnly
from .serializers import ItemCreateUpdateSerializer, ItemDetailSerializer
from shop.models import Shop


class ItemCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    querySet = Item.objects.all()
    serializer_class = ItemCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.get("items") if 'items' in self.request.data else self.request.data
        userDetail = UserDetails.objects.filter(user=request.user).first()
        shop = request.data.get('shop')
        if not userDetail.is_customer:
            shopDetail = Shop.objects.filter(id=self.request.data.get('shop')).first()
            if shopDetail is not None and shopDetail.user == userDetail.user:
                many = isinstance(data, list)
                if many:
                    for x in data:
                        x['shop'] = shop
                serializer = self.get_serializer(data=data, many=many)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                raise NotAcceptable("You are not allowed to create items for other users.")
        else:
            raise NotAcceptable("Customers are not allowed to create shops.")


class ItemUpdateApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Item.objects.all()
    serializer_class = ItemCreateUpdateSerializer
    lookup_field = 'slug'


class ItemDetailApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = 'slug'


class ItemDeleteApiView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Item.objects.all()
    serializer_class = ItemCreateUpdateSerializer
    lookup_field = 'slug'


class ItemShopListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemDetailSerializer

    def get_queryset(self, *args, **kwargs):
        shop_slug = self.kwargs.get('slug')
        queryset = Item.objects.filter(shop__slug__icontains=shop_slug)
        return queryset
