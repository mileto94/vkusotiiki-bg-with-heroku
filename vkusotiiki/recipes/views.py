from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, CategorySerializer, \
    IngredientSerializer, RegionSerializer, DishSerializer, \
    RatingSerializer, RecipeSerializer, \
    RecipeIngredientSerializer, HolidaySerializer

from .models import Ingredient, Category, Region, Dish, \
    Rating, Recipe, RecipeIngredient, Holiday


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows regions to be viewed or edited.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class HolidayViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows holidays to be viewed or edited.
    """
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class DishViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dishes to be viewed or edited.
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rating to be viewed or edited.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

from django.shortcuts import HttpResponse
from firebase.firebase import FirebaseApplication
def test_firebase(request):
    firebase_db = FirebaseApplication('https://vkusotiiki-bg.firebaseio.com/', None)  # no authentication
    users = firebase_db.get('/User', None)
    print(users)
    return HttpResponse('Heeey', {})
