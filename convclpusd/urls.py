from django.urls import path
from .views import ClpToUsd, UsdToClp

urlpatterns = [
    path('clp', UsdToClp.as_view(), name='clp'),
    path('usd', ClpToUsd.as_view(), name='usd'),
]