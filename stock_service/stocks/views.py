# encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response

import pandas as pd
import datetime
import io
import requests
import json


from stocks.producer import publish


import logging

logging.basicConfig()



class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    #HTTP response method
    # def get(self, request, *args, **kwargs):
    #     stock_code = kwargs['str']
    #     stock_url = (f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv")
    #     s=requests.get(stock_url).content
    #     stock_data=pd.read_csv(io.StringIO(s.decode('utf-8')))

    #     #I had to do some work with the date format, converting first from string to date
    #     # and then changingthe dateformat 
    #     stock_data["Date"] = stock_data['Date'].apply(lambda x: pd.to_datetime(x))
    #     stock_data["Date"] = stock_data['Date'].apply(lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ"))

    #     result = stock_data.to_json()
    #     parsed = json.loads(result)

    #     #docker run -it -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    #     connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='localhost'))
    #     channel = connection.channel()

    #     channel.queue_declare(queue='stock')
    #     channel.basic_publish(exchange='', routing_key='stock', body=json.dumps(parsed))
    #     print(" [x] Sent Quote Data", json.dumps(parsed))
    #     connection.close()

    #     return Response(parsed)


    
    def get(self, request, *args, **kwargs):
        stock_code = kwargs['str']
        stock_url = (f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv")
        s=requests.get(stock_url).content
        stock_data=pd.read_csv(io.StringIO(s.decode('utf-8')))

        #I had to do some work with the date format, converting first from string to date
        # and then changingthe dateformat 
        stock_data["Date"] = stock_data['Date'].apply(lambda x: pd.to_datetime(x))
        stock_data["Date"] = stock_data['Date'].apply(lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ"))

        result = stock_data.to_json()
        parsed = json.loads(result)
        publish('stock_check', parsed)

        return Response(parsed)
    