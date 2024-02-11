from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.noticias_financeiras, name='noticias_financeiras'),
]
