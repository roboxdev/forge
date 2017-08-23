# from food.views import FoodCategoryViewSet
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from banka.views import BankaAPIView

router = DefaultRouter()


urlpatterns = [
    url(r'^test/', BankaAPIView.as_view()),
    url(r'^', include(router.urls)),
]
