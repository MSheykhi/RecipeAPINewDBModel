from django.urls import path, include
from rest_framework import routers
# from .views import MovieViewSet, RatingViewSet, UserViewSet
from .views import RecipeViewSet, RatingViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)
router.register('ratings', RatingViewSet)


urlpatterns = [
    path('', include(router.urls))
]
