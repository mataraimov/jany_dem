from django.urls import path, include
from rest_framework import routers

from apps.users.views import PostViewSet

router=routers.DefaultRouter()
router.register(r'posts',PostViewSet)
urlpatterns = [
    path('',include(router.urls)),
]