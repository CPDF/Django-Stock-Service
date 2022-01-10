# encoding: utf-8

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from api import views as api_views

urlpatterns = [
    path('stock/<str>', api_views.StockView.as_view(), name='code'),
    path('history', api_views.HistoryView.as_view(), name='history'),
    path('stats', api_views.StatsView.as_view()),
    path('admin', admin.site.urls),
    path('api-token-auth', obtain_auth_token),
    path('rest-auth', include('rest_auth.urls')),
]
