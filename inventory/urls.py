from django.urls import path
from.views import InventoryList, InventoryDetail

urlpatterns = [
    path('/', InventoryList.as_view(), name='inventory-list'),
    path('<int:pk>/', InventoryDetail.as_view(), name='inventory-detail'),
]
