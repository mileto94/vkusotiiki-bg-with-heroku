from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, CategorySerializer, \
    IngredientSerializer, RegionSerializer, DishSerializer, \
    RatingSerializer, RecipeSerializer, \
    RecipeIngredientSerializer, HolidaySerializer, \
    UserProfileSerializer

from .models import Ingredient, Category, Region, Dish, \
    Rating, Recipe, RecipeIngredient, Holiday, UserProfile

from django.shortcuts import HttpResponse
from firebase.firebase import FirebaseApplication


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        email = data.get('email')
        first_name, last_name = data.get('name', '').split(' ')
        user, cr = User.objects.get_or_create(email=email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'username': email.split('@')[0]
        })
        region, r_cr = Region.objects.get_or_create(
            name=data.get('name')
        )
        userprofile, pr_cr = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'location': region,
                'auth_id': data.get('id')
            }
        )
        request.data['userprofile'] = userprofile
        request.data['region'] = region

        # Validate Recipe
        profile_serializer = UserProfileSerializer(data={
                'auth_id': data.get('id'),
            }
        )
        if profile_serializer.is_valid():
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            profile_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


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

    def list(self, request):
        serializer = IngredientSerializer(Ingredient.objects.all())
        print('ingredient LIST')
        return Response(serializer.data)

    def update(self, request, pk=None):
        print('ingredient Update')
        if pk:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.is_allergic = request.data.get('is_allergic', ingredient.is_allergic)
            ingredient.unit = request.data.get('unit', ingredient.unit)
            ingredient.save()
            return Response(ingredient, status=status.HTTP_201_CREATED)
        return Response(
            # recipe_serializer.errors,
            'Update ingredient',
            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        print('Ingr. create')


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

    def list(self, request):
        serializer = RecipeSerializer(
            Recipe.objects.all(), many=True
        )
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     print('RECIPE Update')
    #     pass

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ingredients_data = data.pop('ingredients', {})

        # Validate Holiday
        if 'holiday' in data.keys():
            holiday = Holiday.objects.filter(id=data.get('holiday')).first()
            if holiday:
                data['holiday'] = holiday
            else:
                return Response(
                    [{'holiday': 'Holiday with this ID does not exist!'}],
                    status=status.HTTP_400_BAD_REQUEST)

        # Validate UserProfile
        user_ser = UserProfileSerializer(data={'auth_id': data.get('user')})
        user_ser.is_valid(raise_exception=True)
        user = UserProfile.objects.get(auth_id=data.get('user'))
        data['user'], request.data['user'] = user, user.id

        # Validate Region
        region = Region.objects.filter(id=data.get('region')).first()
        if region:
            data['region'] = region
        else:
            return Response(
                [{'region': 'Region with this ID does not exist!'}],
                status=status.HTTP_400_BAD_REQUEST)

        # Validate Dish
        dish = Dish.objects.filter(id=data.get('dish')).first()
        if dish:
            data['dish'] = dish
        else:
            return Response(
                [{'dish': 'Dish with this ID does not exist!'}],
                status=status.HTTP_400_BAD_REQUEST)

        # Validate Category
        category = Category.objects.filter(id=data.get('category')).first()
        if category:
            data['category'] = category
        else:
            return Response(
                [{'category': 'Category with this ID does not exist!'}],
                status=status.HTTP_400_BAD_REQUEST)

        # Create Recipe
        recipe, rec_created = Recipe.objects.get_or_create(**data)

        # Validate Ingredients
        for ingr_data in ingredients_data:
            quantity = ingr_data.pop('quantity')
            ingredient, ingr_created = Ingredient.objects.get_or_create(
                name=ingr_data.get('name'),
                defaults={
                    'unit': ingr_data.get('unit'),
                    'is_allergic': ingr_data.get('is_allergic')
                }
            )
            rec_ingr, cr = RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity)

        # Validate Recipe
        recipe_serializer = RecipeSerializer(data=request.data)
        if recipe_serializer.is_valid():
            return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            recipe_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


def test_firebase(request):
    firebase_db = FirebaseApplication('https://vkusotiiki-bg.firebaseio.com/', None)  # no authentication
    users = firebase_db.get('/User', None)
    print(users)
    return HttpResponse('Heeey', {})
