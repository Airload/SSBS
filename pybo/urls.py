from django.urls import path,include

from.import views

urlpatterns = [
    path('',views.index, name='index'),
    path('map/',views.map, name='map'),
    path('data/',views.data, name='data'),
    path('files/',views.files, name='files'),
]