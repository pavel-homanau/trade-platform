from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name='sign up.html')

    def post(self, request):
        user = request.POST
        """{
            'email': request.POST.get('email'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'token': request.POST.get('csrfmiddlewaretoken')
        }"""

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            raise TypeError("Error register")
        else:
            serializer.save()

        return HttpResponseRedirect('/')


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer, TemplateHTMLRenderer)
    serializer_class = LoginSerializer

    def get(self, request):
        return Response(template_name='sign in.html')

    def post(self, request):
        user = request.POST

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            raise TypeError("Error login")
        request.session['is_auth'] = 1
        request.session['current_user'] = user
        return HttpResponseRedirect('/')


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.POST

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SignOutAPIView(APIView):
    def get(self, request):
        del request.session['current_user']
        request.session['is_auth'] = 0

        return HttpResponseRedirect('/')
