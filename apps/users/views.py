from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from django.contrib.auth.views import LoginView
from .permissions import IsAdminOrReadOnly,IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import Post
from django.contrib.auth import logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class MainView(TemplateView):
    template_name = "home.html"
class LoginView(LoginView):
    template_name = "login.html"