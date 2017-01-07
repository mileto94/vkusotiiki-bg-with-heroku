from django.contrib import admin, auth

from .models import Ingredient, Recipe, Category, Region, Rating, Dish, Comment, \
    RecipeIngredient, RecipeImage, Holiday, UserProfile


class UserProfileInlineAdmin(admin.StackedInline):
    model = UserProfile


class UserAdmin(auth.admin.UserAdmin):
    model = auth.models.User
    inlines = auth.admin.UserAdmin.inlines + [UserProfileInlineAdmin, ]

admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)


class RecipeIngredientInlineAdmin(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    fields = ('ingredient', 'quantity')


class RecipeImageInlineAdmin(admin.StackedInline):
    model = RecipeImage
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = (
        'name', 'is_approved', 'region', 'dish', 'difficulty', 'time',
        'modified')
    readonly_fields = ['time', 'modified', 'total_rate']
    list_filter = ('is_approved', 'region', 'dish', 'difficulty')

    inlines = [RecipeIngredientInlineAdmin, RecipeImageInlineAdmin]

admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'unit', 'is_allergic')

admin.site.register(Ingredient, IngredientAdmin)


class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Category, CategoryAdmin)


class RegionAdmin(admin.ModelAdmin):
    model = Region

admin.site.register(Region, RegionAdmin)


class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('value', 'recipe', 'user')

admin.site.register(Rating, RatingAdmin)


class DishAdmin(admin.ModelAdmin):
    model = Dish

admin.site.register(Dish, DishAdmin)


class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Comment, CommentAdmin)


class HolidayAdmin(admin.ModelAdmin):
    model = Holiday

admin.site.register(Holiday, HolidayAdmin)
