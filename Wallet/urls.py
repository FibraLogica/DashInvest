from django.urls import path
from . import views    


urlpatterns = [
    path('carteira/', views.carteira_view, name='carteira_view'),
    ]
