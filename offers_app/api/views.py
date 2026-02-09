from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from offers_app.api.serializers import (
    RetrieveOfferPackageSerializer,
    RetrieveOfferSerializer,
)
from offers_app.models import Offer, OfferPackage


class OfferDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    serializer_class = RetrieveOfferSerializer


class OffersViewSet(ViewSet):
    queryset = OfferPackage.objects.all()

    def list(self, request):
        queryset = OfferPackage.objects.all()
        serializer = RetrieveOfferPackageSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = OfferPackage.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = RetrieveOfferPackageSerializer(
            user, context={"request": request}
        )
        return Response(serializer.data)
