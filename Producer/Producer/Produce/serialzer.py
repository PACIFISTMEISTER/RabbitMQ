from rest_framework import serializers


class URLSer(serializers.Serializer):
    """сериализатор Url"""
    url = serializers.URLField(required=True)
