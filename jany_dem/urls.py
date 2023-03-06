from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from apps.users.views import MainView, user_logout, LoginView
from apps.chat import routing
from apps.chat.routing import websocket_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('',MainView.as_view(),name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
    path('ws/', include((websocket_urlpatterns, 'ws'))),
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
