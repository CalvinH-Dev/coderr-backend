from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from auth_app.api.permissions import (
    IsAdminOrStaff,
    IsBusinessUser,
    IsCustomerUser,
)
from orders_app.api.serializers import (
    CreateOrderSerializer,
    PatchOrderSerializer,
)
from orders_app.models import Order


class OrdersViewSet(ModelViewSet):
    """
    ViewSet for managing orders.

    Provides CRUD operations for orders with role-based permissions.
    Customer users can create orders, business users can update order status,
    and admin/staff can delete orders.
    """

    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PatchOrderSerializer
        return super().get_serializer_class()

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


class OrderCountBusinessAPIView(RetrieveAPIView):
    """
    API view for retrieving total order count for a business user.

    Provides an endpoint to get the total number of orders associated
    with a specific business user.
    """

    def retrieve(self, request, *args, **kwargs):
        business_user_id = kwargs["business_user_id"]
        business_user = get_object_or_404(User, id=business_user_id)

        order_count = business_user.orders_as_business.count()

        return Response(
            {"order_count": order_count}, status=status.HTTP_200_OK
        )


class OrderCountCompletedBusinessAPIView(RetrieveAPIView):
    """
    API view for retrieving completed order count for a business user.

    Provides an endpoint to get the number of completed orders for a
    specific business user.
    """

    def retrieve(self, request, *args, **kwargs):
        business_user_id = kwargs["business_user_id"]
        business_user = get_object_or_404(User, id=business_user_id)

        orders = business_user.orders_as_business.all()
        completed_order_count = orders.filter(status="completed").count()

        return Response(
            {"completed_order_count": completed_order_count},
            status=status.HTTP_200_OK,
        )
