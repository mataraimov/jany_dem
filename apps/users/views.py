from django.views.generic import TemplateView
from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly,IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class MainView(TemplateView):
    template_name = "home.html"