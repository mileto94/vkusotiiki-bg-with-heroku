"""vkusotiiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from rest_framework import routers
from recipes import views


router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'userprofile', views.UserProfileViewSet)
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'dish', views.DishViewSet)
router.register(r'holiday', views.HolidayViewSet)
router.register(r'rating', views.RatingViewSet)
router.register(r'recipe', views.RecipeViewSet)
router.register(r'recipe-new', views.RecipeIngredientViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^filer/', include('filer.urls')),
    url(r'^test_firebase/$', views.test_firebase, name='test_firebase'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
