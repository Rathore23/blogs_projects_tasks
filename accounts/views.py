from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_secure_token.models import Token
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from accounts.models import User
from accounts.permissions import IsSelfOrReadOnly
from accounts.serializers import UserLoginSerializer, UserSerializer


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserAuthViewSet(ViewSet):

    @action(methods=["post"], detail=False,
            permission_classes=[permissions.AllowAny, ],
            url_name="login", url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check credentials
        user = authenticate(request, **serializer.data)
        if not user:
            raise ValidationError("Invalid credentials")
        # Create or Get token for Authentication
        token, _ = Token.objects.get_or_create(user=user)

        user_details = UserSerializer(
            instance=user,
            context={"request": request, "view": self}
        ).data
        user_details["token"] = token.key
        return Response(user_details, status=status.HTTP_202_ACCEPTED)

    @action(methods=["delete"], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_name="logout", url_path="logout")
    def logout(self, request, *args, **kwargs):
        user = request.user
        try:
            Token.objects.filter(user=user).delete()
        except Exception as e:
            raise "Something Went wrong"

        return Response(status=status.HTTP_205_RESET_CONTENT)


class AccountsViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSelfOrReadOnly)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("is_staff", "is_active")
    search_fields = ("username", "phone", "email",)
