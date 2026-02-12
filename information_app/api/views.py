from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from information_app.api.helpers import (
    get_average_rating,
    get_business_profile_count,
    get_offer_count,
    get_review_count,
)


class BaseInfoAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        data = {
            "review_count": get_review_count(),
            "average_rating": get_average_rating(),
            "business_profile_count": get_business_profile_count(),
            "offer_count": get_offer_count(),
        }
        return Response(data, status=status.HTTP_200_OK)
