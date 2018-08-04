from django.urls import path
from .views import dolares_a_pesos, pesos_a_dolares

urlpatterns = [
    path('clp', dolares_a_pesos, name='clp'),
    path('usd', pesos_a_dolares, name='usd'),
]