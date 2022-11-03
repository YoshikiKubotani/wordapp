from django.urls import path

from . import views

urlpatterns = [
    path('', views.TopPage.as_view(), name='home'),
]