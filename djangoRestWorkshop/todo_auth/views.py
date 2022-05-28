from django.contrib.auth import get_user_model, logout, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from djangoRestWorkshop.todo_auth.serializers import CreateUserSerializer, LoginSerializer

UserModel = get_user_model()


class RegisterView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = CreateUserSerializer


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data,
            context={
                'request': request,
            })

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "status": status.HTTP_200_OK,
            "user_id": user.pk,
            "Token": token.key,
        })


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class TestUser(APIView):
    def get(self, request):
        print(request.user)
        return Response({'user': request.user.username})
