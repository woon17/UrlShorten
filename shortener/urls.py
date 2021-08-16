from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:shortened_part>', views.redirectUrlview, name='redirect')
]