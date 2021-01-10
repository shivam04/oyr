from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Shop
from .permissions import IsOwnerOrReadOnly
from .serializers import ShopCreateUpdateSerializer, ShopListSerializer
from account.models import UserDetails


class ShopCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    querySet = Shop.objects.all()
    serializer_class = ShopCreateUpdateSerializer

    def perform_create(self, serializer):
        userDetail = UserDetails.objects.filter(user=self.request.user).first()
        if not userDetail.is_customer:
            serializer.save(user=self.request.user)
        else:
            raise NotAcceptable("Customers are not allowed to create shops.")


class ShopUpdateApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Shop.objects.all()
    serializer_class = ShopCreateUpdateSerializer
    lookup_field = 'slug'


class ShopDetailApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Shop.objects.all()
    serializer_class = ShopCreateUpdateSerializer
    lookup_field = 'slug'


class ShopDeleteApiView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Shop.objects.all()
    serializer_class = ShopCreateUpdateSerializer
    lookup_field = 'slug'


class ShopUserListView(ListAPIView):
    serializer_class = ShopListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Shop.objects.filter(user=self.request.user)
        return queryset

class ShopListView(ListAPIView):
    serializer_class = ShopCreateUpdateSerializer
    permission_classes = []
    queryset = Shop.objects.all()
