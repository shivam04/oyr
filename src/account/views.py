from django.contrib.auth.models import User

# Create your views here.
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, OR
from rest_framework.views import APIView

from .models import UserDetails
from .permissions import IsOwnerOrReadOnly, DeletePermission
from .serializers import UserLoginSerializer, MainUsersDetailSerializer, MainUserDetailCreateUpdateSerializer, \
    UserDetailSerializer, MainUserDetailUpdateSerializer, UserDetailUpdateSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = UserDetails.objects.all()
    serializer_class = MainUsersDetailSerializer
    lookup_field = 'id'


class UserDetailCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserDetails.objects.all()
    serializer_class = MainUserDetailCreateUpdateSerializer


class UserDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = MainUserDetailUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'


class AllUserDetailCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class AllUserDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = UserDetailUpdateSerializer
    lookup_field = 'id'


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def update(self, request, *args, **kwargs):
        self.object = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [DeletePermission]
    serializer_class = UserDetailUpdateSerializer
    lookup_field = 'id'
