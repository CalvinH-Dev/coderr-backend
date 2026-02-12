from django.urls import path
from rest_framework.routers import SimpleRouter

from orders_app.api.views import (
    OrderCountBusinessAPIView,
    OrderCountCompletedBusinessAPIView,
    OrdersViewSet,
)

router = SimpleRouter()
router.register(r"orders", OrdersViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(
        "order-count/<int:business_user_id>/",
        OrderCountBusinessAPIView.as_view(),
        name="order-count",
    ),
    path(
        "completed-order-count/<int:business_user_id>/",
        OrderCountCompletedBusinessAPIView.as_view(),
        name="completed-order-count",
    ),
]
