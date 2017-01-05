from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Ingredient, Category, Region, Dish, Rating, \
    Recipe, RecipeIngredient, Holiday, UserProfile


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    location = RegionSerializer()
    # add image serializer

    class Meta:
        model = UserProfile
        fields = (
            'auth_id', 'is_business', 'phone_number', 'address',
            'location', 'image')


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = (
            'url', 'first_name', 'last_name', 'username', 'email', #'full_name',
            'groups', 'userprofile', 'is_superuser', 'is_staff')

    def create(self, validated_data):
        print(validated_data)
        userprofile = validated_data.pop('userprofile')
        user, _ = User.objects.get_or_create(
            email=validated_data.get('email'),
            defaults=validated_data
        )
        if UserProfile.objects.filter(
            auth_id=userprofile.get('auth_id', None),
            user__email=user.email).exists():
            print('haaaaaaaaaaaaaaaaaaaaaa')


class IngredientSerializer(serializers.ModelSerializer):
    quantity = serializers.CharField(max_length=10, default='')

    class Meta:
        model = Ingredient
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class HolidaySerializer(serializers.HyperlinkedModelSerializer):
    def validate_name(self, name):
        pass

    class Meta:
        model = Holiday
        fields = '__all__'


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def validate_value(self, value):
        """
        Check that the value is a number between 1 and 5.
        """
        if 1 <= float(value) <= 5:
            return value
        raise serializers.ValidationError('Rating value should be between 1 and 5.')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'name', 'description', 'duration', 'difficulty', 'servings',
            'user', 'category', 'dish', 'holiday', 'region', 'ingredients'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        holiday_name = validated_data.pop('holiday', None)
        recipe, rec_created = Recipe.objects.get_or_create(**validated_data)
        if holiday_name is not None:
            holiday, h_ = Holiday.objects.get_or_create(name=holiday_name)
            recipe.holiday = holiday
            recipe.save()
        for ingr_data in ingredients_data:
            quantity = ingr_data.pop('quantity')
            ingredient, ingr_created = Ingredient.objects.get_or_create(**ingr_data)
            rec_ingr, cr = RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity)
        return recipe


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
