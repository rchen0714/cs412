# File: terrier_study/serializer.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This is all the serializers for the terrierstudy application

from rest_framework import serializers
from .models import Building, StudyRoom, UserFavorite, UserReview, UserProfile


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'description',
            'hours_open',
            'image_url',
        ]

    def create(self, validated_data):
        print(f'BuildingSerializer.create, validated_data={validated_data}.')
        return Building.objects.create(**validated_data)


class StudyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyRoom
        fields = [
            'id',
            'building',
            'name',
            'floor',
            'room_number',
            'capacity',
            'description',
            'image_url',
            'on_campus',
            'id_required',
            'wifi',
            'outlets',
            'windows',
            'whiteboard',
        ]

    def create(self, validated_data):
        print(f'StudyRoomSerializer.create, validated_data={validated_data}.')
        return StudyRoom.objects.create(**validated_data)


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavorite
        fields = [
            'id',
            'study_room',
            'user_name',
            'custom_roomname',
            'notes',
            'date_saved',
        ]

    def create(self, validated_data):
        print(f'UserFavoriteSerializer.create, validated_data={validated_data}.')
        return UserFavorite.objects.create(**validated_data)


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = [
            'id',
            'study_room',
            'reviewer_name',
            'rating',
            'text',
            'published',
            'image_url',
        ]

    def create(self, validated_data):
        print(f'UserReviewSerializer.create, validated_data={validated_data}.')
        return UserReview.objects.create(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user_name',
            'bu_id',
            'year',
            'major',
        ]

    def create(self, validated_data):
        print(f'UserProfileSerializer.create, validated_data={validated_data}.')
        return UserProfile.objects.create(**validated_data)