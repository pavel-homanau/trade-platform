from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserSerializer)


class AuthorizationViewSet(viewsets.GenericViewSet):
    default_serializer_class = LoginSerializer
    serializer_classes = {
        'register': RegistrationSerializer,
        'login': LoginSerializer,
    }

    http_method_names = ('post',)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(methods=['POST'], detail=False, url_path='registration')
    def register(self, request):

        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='login')
    def login(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.data)

        request.session['token'] = serializer.data.get('access_token')

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    queryset = User.objects.all()
    serializer_class = UserSerializer
