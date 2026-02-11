from rest_framework.viewsets import ModelViewSet

from orders_app.api.serializers import CreateOrderSerializer
from orders_app.models import Order


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
