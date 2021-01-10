from .views import (
    LoginAPIView,
    UserDetailAPIView,
    UserDetailCreateAPIView,
    AllUserDetailCreateAPIView,
    UserDetailUpdateAPIView,
    AllUserDetailUpdateAPIView,
    ChangePasswordView,
    UserDeleteAPIView
)
from django.urls import path

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('user/<int:id>', UserDetailAPIView.as_view(), name="details"),
    path('user/<int:id>/edit/', UserDetailUpdateAPIView.as_view(), name="update"),
    path('all-user/<int:id>/edit/', AllUserDetailUpdateAPIView.as_view(), name="update-all"),
    path('all-user/<int:id>/delete/', UserDeleteAPIView.as_view(), name="delete"),
    path('all-user/<int:id>/changepassword/', ChangePasswordView.as_view(), name="changepassword"),
    path('user-new/', UserDetailCreateAPIView.as_view(), name="create"),
    path('all-user-new/', AllUserDetailCreateAPIView.as_view(), name="create")
]
