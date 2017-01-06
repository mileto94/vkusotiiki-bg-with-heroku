from django.contrib.auth.models import User
from rest_framework import serializers, validators

from .models import Ingredient, Category, Region, Dish, Rating, \
    Recipe, RecipeIngredient, Holiday, UserProfile


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    location = RegionSerializer(required=False)
    # add image serializer

    class Meta:
        model = UserProfile
        fields = (
            'auth_id', 'is_business', 'phone_number', 'address',
            'location')

    def validate(self, attrs):
        print(attrs)
        user = UserProfile.objects.filter(auth_id=attrs.get('auth_id', None)).first()
        print(user)
        if not user:
            raise serializers.ValidationError(
                {'user': 'UserProfile with this Firebase ID does not exist!'})
        return attrs


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


class HolidaySerializer(serializers.ModelSerializer):
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
            'user', 'category', 'dish', 'holiday', 'region', 'ingredients',
        )


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
