from rest_framework.exceptions import ValidationError


def validate_offer_type(offer_type):
    """
    Validate that the offer type is present and valid.

    Args:
        offer_type: The offer type value to validate.

    Raises:
        ValidationError: If offer_type is missing or not one of the valid types.
    """
    VALID_OFFER_TYPES = {"basic", "standard", "premium"}

    if not offer_type:
        raise ValidationError({"offer_type": "This field is required."})

    if offer_type not in VALID_OFFER_TYPES:
        raise ValidationError(
            {
                "offer_type": f"Invalid value '{offer_type}'. Must be one of: {', '.join(sorted(VALID_OFFER_TYPES))}."  # noqa: E501
            }
        )
