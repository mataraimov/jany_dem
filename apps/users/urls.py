from django.urls import path, include
from rest_framework import routers

from apps.users.views import PostViewSet, PaymentView, register

router=routers.DefaultRouter()
router.register(r'posts',PostViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('posts/<int:pk>/pay/', PaymentView.as_view(), name='post-payment'),
    path('register/',register,name='register')
]