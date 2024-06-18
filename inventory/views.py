from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, isAdminUser
from.models import Inventory
from.serializers import InventorySerializer

class InventoryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class InventoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
