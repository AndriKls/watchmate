from rest_framework import serializers
from ..models import Watchlist, StreamingPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ("watchlist", )
        extra_kwargs = {
            "watchlist": {"write_only": True},
            "active": {"read_only": True},
        }
class WatchlistSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
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
    watchlist= WatchlistSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamingPlatform
        fields = "__all__"




