from .views import (
    ShopCreateAPIView,
    ShopUpdateApiView,
    ShopDetailApiView,
    ShopDeleteApiView,
    ShopUserListView,
    ShopListView
)
from django.urls import path

urlpatterns = [
    path('list/', ShopUserListView.as_view(), name="list"),
    path('all-list/', ShopListView.as_view(), name="list"),
    path('<str:slug>/', ShopDetailApiView.as_view(), name="detail"),
    path('<str:slug>/edit/', ShopUpdateApiView.as_view(), name="update"),
    path('<str:slug>/delete/', ShopDeleteApiView.as_view(), name="delete"),
    path('shop-new/', ShopCreateAPIView.as_view(), name="create"),
]
