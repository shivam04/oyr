from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string
from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from .models import UserDetails


class UserDetailSerializer(ModelSerializer):
    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
            # contact_no = validated_data['contact_no']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',)
        extra_kwargs = {"password":
                            {"write_only": True}
                        }


class UserDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ChangePasswordSerializer(ModelSerializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')


class MainUsersDetailSerializer(ModelSerializer):
    user_detail = SerializerMethodField()

    class Meta:
        model = UserDetails
        fields = [
            'user',
            'user_detail',
            'aadhar_card',
            'contact_no',
            'is_customer'
        ]

    def get_user_detail(self, obj):
        return UserDetailSerializer(obj.user_detail(), many=True).data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            # 'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        # email = data.get("email",None)
        username = data.get("username", None)
        password = data.get("password", None)
        # user_qs = User.objects.filter(email=email)
        if not username:
            raise ValidationError("A usrname  is required to login.")
        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        # user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This Username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect Credentials Please Try again.")
        data['token'] = get_random_string(length=15)
        return data


class MainUserDetailCreateUpdateSerializer(ModelSerializer):
    user_detail = SerializerMethodField()

    class Meta:
        model = UserDetails
        fields = [
            'user',
            'aadhar_card',
            'user_detail',
            'contact_no',
            'is_customer'
        ]

    def get_user_detail(self, obj):
        return UserDetailSerializer(obj.user_detail(), many=True).data


class MainUserDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'aadhar_card',
            'contact_no',
            'is_customer'
        ]


class MainUserDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'aadhar_card',
            'contact_no',
            'is_customer'
        ]
