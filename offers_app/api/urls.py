from django.urls import path
from rest_framework.routers import SimpleRouter

from offers_app.api.views import OfferDetailView, OffersViewSet

router = SimpleRouter()
router.register(r"offers", OffersViewSet, basename="offerpackage")

urlpatterns = router.urls

urlpatterns += [
    path(
        "offerdetails/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail",
    ),
]
