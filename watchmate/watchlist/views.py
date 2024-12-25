# from django.shortcuts import render
# from .models import Movie
# from django.http import JsonResponse
# # Create your views here.

# def movie_list(request):
#     movie_list = Movie.objects.all()
#     data = {"movies": list(movie_list.values("title", "description", "active"))}
    
#     return JsonResponse(data)

# def movie_detail(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {"name": movie.title,
#             "description": movie.description,
#             "active": movie.active}
    
#     return JsonResponse(data)