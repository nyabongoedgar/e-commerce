# wish/views.py
from rest_framework import viewsets
from.models import WishlistItem
from.serializers import WishlistItemSerializer

class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
