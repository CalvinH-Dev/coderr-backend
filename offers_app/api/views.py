from django.db.models import Min
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.api.permissions import (
    IsAdminOrStaff,
    IsBusinessUser,
)
from offers_app.api.pagination import (
    OfferPackageSetPagination,
)
from offers_app.api.permissions import IsOfferOwner
from offers_app.api.query import (
    filter_creator,
    filter_max_delivery_time,
    filter_min_price,
    filter_search,
    get_query_param_values,
    order_queryset,
)
from offers_app.api.serializers import (
    CreateOrUpdateOfferPackageSerializer,
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
        queryset = queryset.annotate(
            min_delivery_time=Min("offers__delivery_time_in_days"),
            min_price=Min("offers__price"),
        )
        queryset = queryset.annotate(min_price=Min("offers__price"))
        query_params = [
            "creator_id",
            "min_price",
            "max_delivery_time",
            "search",
            "ordering",
        ]
        query_param_values = get_query_param_values(self.request, query_params)
        queryset = filter_creator(queryset, query_param_values["creator_id"])
        queryset = filter_min_price(queryset, query_param_values["min_price"])
        queryset = filter_max_delivery_time(
            queryset, query_param_values["max_delivery_time"]
        )
        queryset = filter_search(queryset, query_param_values["search"])
        queryset = order_queryset(queryset, query_param_values["ordering"])
        return queryset

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "list":
            return [AllowAny()]

        if self.action == "create":
            return [IsAuthenticated(), IsBusinessUser()]

        if self.action == "partial_update":
            return [IsAuthenticated(), IsOfferOwner()]

        if self.action == "destroy":
            return [IsAdminOrStaff()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return ListOfferPackageSerializer
        if self.action == "retrieve":
            return RetrieveOfferPackageSerializer
        if self.action in ("create", "partial_update"):
            return CreateOrUpdateOfferPackageSerializer
        return RetrieveOfferPackageSerializer
