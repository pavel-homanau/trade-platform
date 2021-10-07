from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User


class IndexAPIView(APIView):

    def get(self, request):
        try:
            is_auth = request.session['is_auth']
        except AttributeError:
            is_auth = 0
        current_username = User.objects.get(email=request.session['current_user']['email']).username

        return render(request,
                      'index.html',
                      context={'is_auth': is_auth,
                               'current_user_username': current_username})
