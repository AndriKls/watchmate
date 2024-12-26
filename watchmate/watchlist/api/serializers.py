from rest_framework import serializers
from ..models import Watchlist, StreamingPlatform

class WatchlistSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    class Meta:
        model = Watchlist
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "title": {"required": True},
            "description": {"required": True},
            "active": {"required": True},
        }
        
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError("Title and Description should be different")
        if len(data['title']) < 2:
            raise serializers.ValidationError("Title is too short")
        return data
    

class StreamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = "__all__"
    
    # def get_len_name(self, object):
    #     return len(object.title)

# def title_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Title is too short")
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[title_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         return data
    
    # def validate_title(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     return value
    