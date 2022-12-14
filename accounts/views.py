from django.contrib.auth import authenticate

from rest_framework.views import APIView, Request, Response, status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser

from accounts.permissions import IsAccountOwner

from .serializers import AccountSerializer, IsActiveSerializer, LoginSerializer

from .models import Account

class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetailView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        newest_user = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:newest_user]

class LoginView(APIView):
    queryset = Token.objects.all()
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serialized_login = LoginSerializer(data=request.data)
        serialized_login.is_valid(raise_exception=True)

        user = authenticate(
            username=serialized_login.validated_data["username"],
            password=serialized_login.validated_data["password"]
        )

        if not user:
            return Response({"detail": "invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

class AccountUpdateView(UpdateAPIView):
    permission_classes = [IsAccountOwner]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class ManagementView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Account.objects.all()
    serializer_class = IsActiveSerializer