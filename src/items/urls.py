from .views import (
    ItemCreateAPIView,
    ItemUpdateApiView,
    ItemDetailApiView,
    ItemDeleteApiView,
    ItemShopListAPIView
)
from django.urls import path

urlpatterns = [
    path('shop/<str:slug>/', ItemShopListAPIView.as_view(), name="create"),
    path('<str:slug>/', ItemDetailApiView.as_view(), name="detail"),
    path('<str:slug>/edit/', ItemUpdateApiView.as_view(), name="update"),
    path('<str:slug>/delete/', ItemDeleteApiView.as_view(), name="delete"),
    path('item-new/', ItemCreateAPIView.as_view(), name="create"),
]
