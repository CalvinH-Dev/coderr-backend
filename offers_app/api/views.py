from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from offers_app.api.filtering import filter_creator
from offers_app.api.pagination import (
    OfferPackageSetPagination,
)
from offers_app.api.serializers import (
    ListOfferPackageSerializer,
    RetrieveOfferPackageSerializer,
    RetrieveOfferSerializer,
)
from offers_app.models import Offer, OfferPackage


class OfferDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    serializer_class = RetrieveOfferSerializer


class OffersViewSet(ModelViewSet):
    pagination_class = OfferPackageSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OfferPackage.objects.all().order_by("-created_at")
        creator_id = self.request.query_params.get("creator_id")
        queryset = filter_creator(queryset, creator_id)
        return queryset

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "list":
            return [AllowAny()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return ListOfferPackageSerializer
        if self.action == "retrieve":
            return RetrieveOfferPackageSerializer
        return RetrieveOfferPackageSerializer
