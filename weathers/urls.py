from django.urls import path
from .import views

urlpatterns=[
    path('delete/<city_name>/', views.delete_city , name='delete_city' ),
    path('', views.index,name='home'),
]