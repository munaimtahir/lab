"""URL patterns for settings app."""

from django.urls import path

from .views import (
    RolePermissionListView,
    RolePermissionUpdateView,
    WorkflowSettingsView,
)

urlpatterns = [
    path("workflow/", WorkflowSettingsView.as_view(), name="workflow-settings"),
    path("permissions/", RolePermissionListView.as_view(), name="permissions-list"),
    path(
        "permissions/update/",
        RolePermissionUpdateView.as_view(),
        name="permissions-update",
    ),
]
