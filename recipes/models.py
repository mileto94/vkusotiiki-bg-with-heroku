from collections import OrderedDict

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from filer.fields.image import FilerImageField


DIFFICULTIES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)


class UserProfile(models.Model):
    """
    Description: Advanced User Profile model
    """
    user = models.OneToOneField(User)
    auth_id = models.CharField(
        default='',
        max_length=75,
        verbose_name='Firebase ID')
    image = FilerImageField(
        related_name="user_image",
        blank=True,
        null=True)
    location = models.ForeignKey(
        'Region',
        null=True)
    is_business = models.BooleanField(default=False)
    phone_number = models.CharField(
        default='',
        blank=True,
        null=True,
        max_length=15,
        verbose_name='Phone number for business users.')
    address = models.CharField(
        default='',
        blank=True,
        null=True,
        max_length=200,
        verbose_name='Address for business users.')
    recipes = models.ManyToManyField('Recipe', blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def get_serialized(self):
        return OrderedDict({
            "id": self.auth_id,
            "is_business": self.is_business,
            "phone_number": self.phone_number,
            "address": self.address,
            "region": {
                "id": self.location.id,
                "name": self.location.name
            },
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "name": self.user.get_full_name(),
            "username": self.user.username,
            "email": self.user.email,
            "is_superuser": self.user.is_superuser,
            "is_staff": self.user.is_staff,
            "favourites": self.recipes.values_list('id', flat=True),
        })


class Category(models.Model):
    """
    Description: Represent a single category.
    """
    name = models.CharField(default='', max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Ingredient(models.Model):
    """
    Description: Represent a single ingredient.
    """
    name = models.CharField(default='', max_length=50)
    is_allergic = models.BooleanField(default=False)
    unit = models.CharField(default='', max_length=10)

    def __unicode__(self):
        return self.name

    @property
    def quantity(self):
        """Dummy method to allow to save quantity for recipe ingredient."""
        pass

    @quantity.setter
    def quantity(self, val):
        """Dummy method to allow to save quantity for recipe ingredient."""
        pass


class Region(models.Model):
    """
    Description: Represent a single region.
    """
    name = models.CharField(default='', max_length=50)

    def __unicode__(self):
        return self.name


class Holiday(models.Model):
    """
    Description: Represent a single region.
    """
    name = models.CharField(default='', max_length=50)

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    """
    Description: Represent a single rating object.
    """
    user = models.ForeignKey(UserProfile)
    recipe = models.ForeignKey('Recipe', related_name='ratings')
    value = models.DecimalField(
        default=0.0,
        max_digits=5,
        decimal_places=1)

    def __unicode__(self):
        return str(self.value)


class Dish(models.Model):
    """
    Description: Represent a single region.
    """
    name = models.CharField(default='', max_length=50)

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'

    def __unicode__(self):
        return self.name


class RecipeImage(models.Model):
    image = FilerImageField(
        related_name="img",
        blank=True,
        null=True)
    recipe = models.ForeignKey('Recipe')


class Recipe(models.Model):
    """
    Description: Represents a single recipe.
    """
    name = models.CharField(
        default='',
        max_length=100)

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient')

    description = models.TextField()

    difficulty = models.PositiveSmallIntegerField(
        choices=DIFFICULTIES,
        default=DIFFICULTIES[0][0])

    servings = models.PositiveSmallIntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile)
    category = models.ForeignKey(Category)
    region = models.ForeignKey(Region, verbose_name='Region')
    duration = models.CharField(default='', max_length=20)

    dish = models.ForeignKey(
        Dish,
        verbose_name='Type of dish')

    holiday = models.ForeignKey(
        Holiday,
        blank=True,
        null=True,
        verbose_name='Prepared for holiday')

    time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date created')

    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Date modified')

    def __unicode__(self):
        return self.name

    @property
    def total_rate(self):
        ratings = self.ratings.values_list('value', flat=True)
        if len(ratings):
            return sum(ratings) / len(ratings)
        return 0


class RecipeIngredient(models.Model):
    """
    Description: Represent the relation between recipe and its ingredients.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients',
        on_delete=models.CASCADE)

    recipe = models.ForeignKey(
        Recipe,
        related_name='recipes',
        on_delete=models.CASCADE)

    quantity = models.CharField(default='', max_length=10)

    def __unicode__(self):
        return u'{} {} {}'.format(self.ingredient.name, self.quantity, self.ingredient.unit)


class Comment(models.Model):
    """
    Description: Represent a single comment.
    """
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(UserProfile)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.recipe
