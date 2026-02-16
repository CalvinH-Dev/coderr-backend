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
    CreateOfferPackageSerializer,
    ListOfferPackageSerializer,
    RetrieveOfferPackageSerializer,
    RetrieveOfferSerializer,
    UpdateOfferPackageSerializer,
)
from offers_app.models import Offer, OfferPackage


class OfferDetailView(RetrieveAPIView):
    """
    API view for retrieving individual offer details.

    Provides a read-only endpoint for authenticated users to view
    detailed information about a specific offer.
    """

    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    serializer_class = RetrieveOfferSerializer


class OffersViewSet(ModelViewSet):
    """
    ViewSet for managing offer packages.

    Provides CRUD operations for offer packages with support for filtering,
    searching, ordering, and pagination. Permissions vary by action type.

    Supported query parameters:
        - creator_id: Filter by user ID of the creator.
        - min_price: Filter by minimum price threshold.
        - max_delivery_time: Filter by maximum delivery time.
        - search: Search in title and description fields.
        - ordering: Order by 'min_price' or 'updated_at'.
        - page_size: Amount of items per page.
    """

    pagination_class = OfferPackageSetPagination

    def get_queryset(self):
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
        if self.action == "create":
            return CreateOfferPackageSerializer
        if self.action == "partial_update":
            return UpdateOfferPackageSerializer
        return RetrieveOfferPackageSerializer
