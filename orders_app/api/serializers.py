from offers_app.api.serializers import RetrieveOfferSerializer
from offers_app.models import Offer


class CreateOrderSerializer(RetrieveOfferSerializer):
    class Meta(RetrieveOfferSerializer.Meta):
        model = Offer
        fields = RetrieveOfferSerializer.Meta.fields + []
