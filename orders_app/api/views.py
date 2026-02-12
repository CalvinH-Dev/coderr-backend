from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.api.permissions import (
    IsAdminOrStaff,
    IsBusinessUser,
    IsCustomerUser,
)
from orders_app.api.serializers import CreateOrderSerializer
from orders_app.models import Order


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated(), IsCustomerUser()]
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action == "destroy":
            return [IsAdminOrStaff()]
        return super().get_permissions()
