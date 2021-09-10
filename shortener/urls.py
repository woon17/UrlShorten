from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:shortened_part>/', views.redirectUrlview, name='redirect'),
    # path('/api/getshorturl/(?P<intentId>\w{0,50})', views.apiGetShortUrl),
    path('api/getshorturl/', views.apiGetShortUrl, name='apiGetshortUrl'),
]