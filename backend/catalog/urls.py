"""URL configuration for catalog app."""

from django.urls import path

from .views import TestCatalogDetailView, TestCatalogListCreateView

urlpatterns = [
    path("", TestCatalogListCreateView.as_view(), name="test-catalog-list"),
    path("<int:pk>/", TestCatalogDetailView.as_view(), name="test-catalog-detail"),
]
