from rest_framework import serializers


class URLSer(serializers.Serializer):
    url = serializers.URLField(required=True)
