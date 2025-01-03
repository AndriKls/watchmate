from ..models import Watchlist, StreamingPlatform, Review
from .serializers import StreamingPlatformSerializer, ReviewSerializer, WatchlistSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter()
    
    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        watchlist = Watchlist.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data["rating"]) / 2
        
        watchlist.number_rating += 1
        serializer.save(watchlist=watchlist, review_user=review_user)
        watchlist.save()


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)



class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


class StreamingPlatformViewSet(viewsets.ViewSet):
    
    def list(self, request):
        platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(platforms, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = StreamingPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamingPlatformSerializer(watchlist)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=204)


class WatchlistView(APIView):
    def get(self, request):
        movies = Watchlist.objects.all()
        serializer = WatchlistSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class WatchlistDetails(APIView):
    def get(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(movie)
            return Response(serializer.data, status=200)
        except Watchlist.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)
    
    def put(self, request, pk):
        movie = Watchlist.objects.get(pk=pk)
        serializer = WatchlistSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        movie = Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=204)
