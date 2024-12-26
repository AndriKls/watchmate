from django.urls import path
from .views import WatchlistView, WatchlistDetails, StreamingPlatformView, StreamingPlatformDetails

urlpatterns = [
    path('list/', WatchlistView.as_view(), name='movie-list'),
    path('<int:pk>/', WatchlistDetails.as_view(), name='movie-detail'),
    path('platforms/list/', StreamingPlatformView.as_view(), name='streaming-platform-list'),
    path('platforms/<int:pk>/', StreamingPlatformDetails.as_view(), name='streaming-platform-detail'),
    
]
