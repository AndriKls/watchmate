from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewList, ReviewDetails, ReviewCreate, StreamingPlatformViewSet, WatchlistDetails, WatchlistView

router = DefaultRouter()
router.register('stream', StreamingPlatformViewSet, basename='stream')
urlpatterns = [
    path('list/', WatchlistView.as_view(), name='watchlist'),
    path('<int:pk>', WatchlistDetails.as_view(), name='watchlist-details'),
    
    path('', include(router.urls)),
    
    path('<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),
    path('api-auth/', include('rest_framework.urls'))
]
