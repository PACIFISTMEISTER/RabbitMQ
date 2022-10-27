from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzer import URLSer
import pika
conn_params=pika.ConnectionParameters('localhost')


class URLView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serial = URLSer(data=data)
        if serial.is_valid(raise_exception=True):
            SendMessage(serial.validated_data['url'])
            return Response({'Message': 'Req sent'})
        return Response({'Message': 'Data not Valid'})


def SendMessage(url: str):
    conn = pika.BlockingConnection(conn_params)
    channel = conn.channel()
    channel.queue_declare('Messages')
    channel.basic_publish(exchange='',routing_key='Messages',body=bytes(url, encoding='utf8'))
    print('mes sent',url)
    conn.close()