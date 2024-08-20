from django.urls import path
from .views import GenerateBillView

urlpatterns = [
    path('generate-bill/', GenerateBillView.as_view(), name='generate-bill'),
]
