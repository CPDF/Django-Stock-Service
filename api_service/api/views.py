# encoding: utf-8

import json
import requests
import pandas as pd
from datetime import datetime
import pika, sys, os

from rest_framework import generics
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.db.models import Count, query


from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer

class StockView(APIView):
    
    def __init__(self):
        self.response_string = ""

    """
    Endpoint to allow users to query stocks
    """
    
    permissions_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        account = User.objects.get(auth_token=request.auth)
        
        stock_code = kwargs['str']
        
        #This is calling the "stock_service" served in the another Django project or service
        request=requests.get(f'http://localhost:8001/stock/{stock_code}', verify=False)

        #Connect with the rabbitmq server and retrieve the message
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='django-challenge_rabbitmq_django'))
        channel = connection.channel()
        channel.queue_declare(queue='stock')

        
        channel.basic_consume(queue='stock', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

        request = json.loads(self.response_string)
        #print("RESPONSE: ", dir(request.content), type(request.content))
        #json_request = json.loads(request.content)
        
        query_date = datetime.now()

        request["date_query"] = query_date     
        request["user"] = account.pk

        query_data = {  
                "date":request["Date"]['0'],
                "date_query":query_date,
                "name":request["Name"]['0'],
                "symbol":request["Symbol"]['0'], 
                "open":request["Open"]['0'],
                "high":round(request["High"]['0'],2),
                "low":round(request["Low"]['0'],2),
                "close":request["Close"]['0'],
                "user":account.pk,
                }
                
        serializer = UserRequestHistorySerializer(data=query_data)
        
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save()
            return Response(query_data)
        return Response(query_data)

    
    #RabbitMQ consumer
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        self.response_string = body
        ch.stop_consuming()
        return body




class HistoryView(generics.ListAPIView):

    """
    Returns queries made by current user.
    """
    permissions_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        account = User.objects.get(auth_token=request.auth)
        pk = account.pk
        query_set = UserRequestHistory.objects.filter(user=pk).order_by('date_query')
        response_json = {}

        for index, query_value in enumerate(query_set):
            #For the sake of brevity, I'll leave for now only a few data fields
            #The idea is to use them all when the interface is made
            response_json[index] = {"name":query_value.name, "date":query_value.date, "symbol":query_value.symbol}

        return Response(response_json)



class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        #We use aggregation
        query_count = UserRequestHistory.objects.values_list('symbol').annotate(symbol_count=Count('symbol')).order_by('-symbol_count')[0:5]
        return Response(query_count)
