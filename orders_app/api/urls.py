from rest_framework.routers import SimpleRouter

from orders_app.api.views import OrdersViewSet

router = SimpleRouter()
router.register(r"orders", OrdersViewSet)

urlpatterns = router.urls
