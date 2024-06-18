# wish/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from.views import WishlistItemViewSet

router = DefaultRouter()
router.register(r'wishlistitems', WishlistItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
