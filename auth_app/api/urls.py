from django.urls import path

from auth_app.api.views import (
    BusinessProfilesView,
    CustomerProfilesView,
    LoginView,
    ProfileDetailView,
    RegistrationView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "profile/<int:id>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "profile/business/",
        BusinessProfilesView.as_view(),
        name="profile-business-list",
    ),
    path(
        "profile/customer/",
        CustomerProfilesView.as_view(),
        name="profile-customer-list",
    ),
]
