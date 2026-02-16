"""
Base test case class with pre-configured test data.

This module provides a custom APITestCase class that sets up a comprehensive
test environment with users, profiles, offers, orders, and reviews for testing
Django REST Framework applications.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from offers_app.models import Offer, OfferPackage
from orders_app.models import Order
from reviews_app.models import Review


class APITestCaseWithSetup(APITestCase):
    """
    Extended APITestCase with pre-configured test data.

    This class extends Django REST Framework's APITestCase and provides a
    comprehensive set of test data including business users, customer users,
    offers, orders, and reviews. All test data is created once per test class
    using setUpTestData for improved test performance.

    Class Attributes:
        business_user_1 (User): First business user account.
        business_profile_1 (UserProfile): Profile for first business user.
        offer_package_1 (OfferPackage): Web development offer package.
        basic_web_offer (Offer): Basic tier web development offer.
        standard_web_offer (Offer): Standard tier web development offer.
        premium_web_offer (Offer): Premium tier web development offer.
        business_user_2 (User): Second business user account.
        business_profile_2 (UserProfile): Profile for second business user.
        offer_package_2 (OfferPackage): Graphic design offer package.
        basic_design_offer (Offer): Basic tier graphic design offer.
        standard_design_offer (Offer): Standard tier graphic design offer.
        premium_design_offer (Offer): Premium tier graphic design offer.
        customer_user_1 (User): First customer user account.
        customer_profile_1 (UserProfile): Profile for first customer user.
        customer_user_2 (User): Second customer user account.
        customer_profile_2 (UserProfile): Profile for second customer user.
        order_1 (Order): In-progress order for standard web package.
        order_2 (Order): In-progress order for basic design package.
        order_3 (Order): Cancelled order for premium design package.
        order_4 (Order): Completed order for premium web package.
        review_1 (Review): 5-star review for business_user_1.
        review_2 (Review): 4-star review for business_user_1.
        review_3 (Review): 3-star review for business_user_2.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create test data for all test cases in the class.

        This method is called once per test class to create a comprehensive
        set of test data including users, profiles, offers, orders, and reviews.
        The data is shared across all test methods in the class for improved
        performance.

        Creates:
            - 2 business users with profiles and offer packages
            - 6 offers (3 web development, 3 graphic design)
            - 2 customer users with profiles
            - 4 orders with different statuses
            - 3 reviews with different ratings
        """
        cls.business_user_1 = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        cls.business_profile_1 = UserProfile.objects.create(
            user=cls.business_user_1,
            type="business",
            tel="123456789",
            location="Berlin",
            description="Business User 1",
            file="laughing.jpg",
            working_hours="5-17",
        )
        cls.offer_package_1 = OfferPackage.objects.create(
            user=cls.business_user_1, title="Web Development Package"
        )
        cls.basic_web_offer = Offer.objects.create(
            title="Basic Web Package",
            delivery_time_in_days=5,
            revisions=2,
            price=100.10,
            offer_type="basic",
            features=["WebDev", "Responsive"],
            package=cls.offer_package_1,
        )
        cls.standard_web_offer = Offer.objects.create(
            title="Standard Web Package",
            delivery_time_in_days=10,
            revisions=5,
            price=250,
            offer_type="standard",
            features=["WebDev", "Responsive", "SEO"],
            package=cls.offer_package_1,
        )
        cls.premium_web_offer = Offer.objects.create(
            title="Premium Web Package",
            delivery_time_in_days=15,
            revisions=10,
            price=500,
            offer_type="premium",
            features=["WebDev", "Responsive", "SEO", "Analytics"],
            package=cls.offer_package_1,
        )

        cls.business_user_2 = User.objects.create_user(
            username="sarah_miller",
            email="sarah.miller@example.com",
            first_name="Sarah",
            last_name="Miller",
            password="testpass123",
        )
        cls.business_profile_2 = UserProfile.objects.create(
            user=cls.business_user_2,
            type="business",
            tel="987654321",
            location="Munich",
            description="Business User 2",
            file="smiling.jpg",
            working_hours="9-18",
        )
        cls.offer_package_2 = OfferPackage.objects.create(
            user=cls.business_user_2, title="Graphic Design Package"
        )
        cls.basic_design_offer = Offer.objects.create(
            title="Basic Design",
            delivery_time_in_days=3,
            revisions=1,
            price=80,
            offer_type="basic",
            features=["Logo", "Business Card"],
            package=cls.offer_package_2,
        )
        cls.standard_design_offer = Offer.objects.create(
            title="Standard Design",
            delivery_time_in_days=7,
            revisions=3,
            price=200,
            offer_type="standard",
            features=["Logo", "Business Card", "Letterhead"],
            package=cls.offer_package_2,
        )
        cls.premium_design_offer = Offer.objects.create(
            title="Premium Design",
            delivery_time_in_days=14,
            revisions=8,
            price=450,
            offer_type="premium",
            features=["Logo", "Business Card", "Letterhead", "Flyer"],
            package=cls.offer_package_2,
        )

        cls.customer_user_1 = User.objects.create_user(
            username="alice_customer",
            email="alice@example.com",
            first_name="Alice",
            last_name="Customer",
            password="testpass123",
        )
        cls.customer_profile_1 = UserProfile.objects.create(
            user=cls.customer_user_1,
            type="customer",
            tel="111222333",
            location="Hamburg",
            description="Customer User 1",
        )

        cls.customer_user_2 = User.objects.create_user(
            username="bob_customer",
            email="bob@example.com",
            first_name="Bob",
            last_name="Customer",
            password="testpass123",
        )
        cls.customer_profile_2 = UserProfile.objects.create(
            user=cls.customer_user_2,
            type="customer",
            tel="444555666",
            location="Frankfurt",
            description="Customer User 2",
        )

        cls.order_1 = Order.objects.create(
            business_user=cls.business_user_1,
            customer_user=cls.customer_user_1,
            title=cls.standard_web_offer.title,
            revisions=cls.standard_web_offer.revisions,
            delivery_time_in_days=cls.standard_web_offer.delivery_time_in_days,
            offer_type=cls.standard_web_offer.offer_type,
            price=cls.standard_web_offer.price,
            features=cls.standard_web_offer.features,
            status="in_progress",
        )

        cls.order_2 = Order.objects.create(
            business_user=cls.business_user_1,
            customer_user=cls.customer_user_2,
            title=cls.basic_design_offer.title,
            revisions=cls.basic_design_offer.revisions,
            delivery_time_in_days=cls.basic_design_offer.delivery_time_in_days,
            offer_type=cls.basic_design_offer.offer_type,
            price=cls.basic_design_offer.price,
            features=cls.basic_design_offer.features,
            status="in_progress",
        )

        cls.order_3 = Order.objects.create(
            business_user=cls.business_user_2,
            customer_user=cls.customer_user_1,
            title=cls.premium_design_offer.title,
            revisions=cls.premium_design_offer.revisions,
            delivery_time_in_days=cls.premium_design_offer.delivery_time_in_days,
            offer_type=cls.premium_design_offer.offer_type,
            price=cls.premium_design_offer.price,
            features=cls.premium_design_offer.features,
            status="cancelled",
        )

        cls.order_4 = Order.objects.create(
            business_user=cls.business_user_1,
            customer_user=cls.customer_user_2,
            title=cls.premium_web_offer.title,
            revisions=cls.premium_web_offer.revisions,
            delivery_time_in_days=cls.premium_web_offer.delivery_time_in_days,
            offer_type=cls.premium_web_offer.offer_type,
            price=cls.premium_web_offer.price,
            features=cls.premium_web_offer.features,
            status="completed",
        )

        cls.review_1 = Review.objects.create(
            business_user=cls.business_user_1,
            reviewer=cls.customer_user_1,
            rating=5,
            description="Excellent work! Very professional and delivered on time.",
        )

        cls.review_2 = Review.objects.create(
            business_user=cls.business_user_1,
            reviewer=cls.customer_user_2,
            rating=4,
            description="Good quality work, communication could be better.",
        )

        cls.review_3 = Review.objects.create(
            business_user=cls.business_user_2,
            reviewer=cls.customer_user_1,
            rating=3,
            description="Average experience, took longer than expected.",
        )
