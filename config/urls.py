from django.contrib import admin
from django.urls import path, include
from pybo import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('users/', include('users.urls')),
    path('post/',include('support.urls')),
    path('report/',include('report.urls')),
]

