from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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
    queryset = OfferPackage.objects.all()

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
