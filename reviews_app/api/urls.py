from rest_framework.routers import SimpleRouter

from reviews_app.api.views import ReviewsViewSet

router = SimpleRouter()
router.register(r"reviews", ReviewsViewSet)

urlpatterns = router.urls
