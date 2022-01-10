# encoding: utf-8

from django.urls import path

from stocks import views as stocks_views

urlpatterns = [
    path('stock/<str>', stocks_views.StockView.as_view(), name='code'),
]
