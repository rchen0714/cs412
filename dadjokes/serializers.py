"""
File: dadjokes/serializers.py
Author: Ruby Chen (rc071404@bu.edu)
Date: 11/16/2025
Description: Django REST Framework serializers for converting Joke and 
Picture model instances into JSON for API responses and to validate 
incoming POST data.
"""

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']

    def create(self, validated_data):
        print(f'JokeSerializer.create, validated_data={validated_data}.')
        return Joke.objects.create(**validated_data)




class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']

    def create(self, validated_data):
        print(f'PictureSerializer.create, validated_data={validated_data}.')
        return Picture.objects.create(**validated_data)