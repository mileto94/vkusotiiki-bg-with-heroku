from django.contrib.auth.models import User
from rest_framework import serializers, validators

from .models import Ingredient, Category, Region, Dish, Rating, \
    Recipe, RecipeIngredient, Holiday, UserProfile


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

    def validate_name(self, val):
        if not val or Region.objects.filter(name=val).exists():
            raise serializers.ValidationError(
                'A region with this name already exists!')
        return val


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email',
            'is_superuser', 'is_staff')

    def validate_email(self, email):
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError('A user with this email is already registered!')
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).first():
            raise serializers.ValidationError('A user with this username is already registered!')
        return username


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    location = RegionSerializer(required=False)
    # add image serializer

    class Meta:
        model = UserProfile
        fields = (
            'auth_id', 'is_business', 'phone_number', 'address',
            'location', 'user')

    def validate(self, attrs):
        print(attrs)
        user_profile = UserProfile.objects.filter(auth_id=attrs.get('auth_id', None)).first()
        print(user_profile)
        if not user_profile:
            raise serializers.ValidationError(
                {'auth_id': 'UserProfile with this Firebase ID does not exist!'})

        return attrs


class IngredientSerializer(serializers.ModelSerializer):
    # quantity = serializers.CharField(max_length=10, default='')

    class Meta:
        model = Ingredient
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, val):
        if not val or Category.objects.filter(name=val).exists():
            raise serializers.ValidationError(
                'A category with this name already exists!')
        return val


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

    def validate_name(self, val):
        if not val or Dish.objects.filter(name=val).exists():
            raise serializers.ValidationError(
                'A dish with this name already exists!')
        return val


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'

    def validate_name(self, val):
        if not val or Holiday.objects.filter(name=val).exists():
            raise serializers.ValidationError(
                'A holiday with this name already exists!')
        return val


class RatingSerializer(serializers.ModelSerializer):
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
        # fields = (
        #     'name', 'description', 'duration', 'difficulty', 'servings',
        #     'user', 'category', 'dish', 'region', 'ingredients'
        # )
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
