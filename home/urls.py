from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('analytics/<str:symbol>/', views.Analytics, name='analytics'),
    path('get-stock-plots/<str:symbol>/', views.get_stock_plots, name='get_stock_plots'),
    path('get-latest-news/<str:symbol>/', views.get_latest_news, name='get_latest_news'),
]