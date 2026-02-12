from django.urls import path

from information_app.api.views import BaseInfoAPIView

urlpatterns = [path("base-info/", BaseInfoAPIView.as_view(), name="base-info")]
