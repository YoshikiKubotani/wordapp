from django.urls import path

from . import views

urlpatterns = [
    path('', views.StartPage.as_view(), name='start'),
    path('genra', views.GenraPage.as_view(), name='genra'),
    path('wordlevel', views.WordLevelPage.as_view(), name='wordlevel'),
    path('solve', views.SolvePage.as_view(), name='solve'),
    path('result', views.ResultPage.as_view(), name='result'),
]