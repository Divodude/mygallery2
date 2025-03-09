from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from foto.models import dataset
from datetime import datetime



class mySerializer(serializers.ModelSerializer):
    class Meta:
        model=dataset
        fields="__all__"
    
    def create(self, validated_data):
        return dataset.objects.update_or_create(**validated_data)

    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.date = validated_data.get('date', instance.date)
        instance.event = validated_data.get('event', instance.event)
        instance.name = validated_data.get('name', instance.name)
        instance.likes = validated_data.get('likes', instance.likes)
        if 'images' in validated_data:
            instance.images = validated_data.get('images')
        
        instance.save()
        return instance

    
     

