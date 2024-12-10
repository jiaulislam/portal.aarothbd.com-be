from django.urls import path

from .views import CountryListView

urlpatterns = [
    path(r"countries/", CountryListView.as_view(), name="country-list"),
]
