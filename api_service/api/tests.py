from django.test import TestCase

from api.views import StockView
import json
import requests


object_name_achvus = {"Symbol":{"0":"ACHV.US"},"Date":{"0":"2021-12-06T00:00:00Z"},"Time":{"0":"21:54:05"},"Open":{"0":6.92},"High":{"0":7.0999},"Low":{"0":6.55},"Close":{"0":6.88},"Volume":{"0":89520},"Name":{"0":"ACHIEVE LIFE SCIENCES"}}

class StockViewTest(TestCase):
    def test_get_stock_data(self):

        url = "http://127.0.0.1:8000/stock/ACHV.US"

        payload={}
        headers = {
        'Authorization': 'Token dfd7c91b7be9673ebaedb61799ffbaca3e96e3a0'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
        #Check if the response gives the expected symbol
        self.assertEqual(response["symbol"], object_name_achvus["Symbol"]['0'])
