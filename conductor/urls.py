from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"pipeline", views.ConductorPipelineView)
router.register(r"pipeline/new", views.ConductorPipelineNewView)
router.register(r"pipeline/delete", views.ConductorPipelineDeleteView)
router.register(r"pipeline/rename", views.ConductorPipelineRenameView)
router.register(
    r"pipeline/component-instance",
    views.ConductorPipelineComponentInstanceView,
)
router.register(
    r"pipeline/component-instance/new/(?P<pk>\d+)",
    views.ConductorPipelineComponentInstanceNewView,
)
router.register(
    r"pipeline/component-instance/delete",
    views.ConductorPipelineComponentInstanceDeleteView,
)
router.register(
    r"component/details",
    views.ConductorComponentDetailsView,
)

urlpatterns = [
    *router.urls,
    path(
        "component/search/",
        views.ConductorComponentSearchView.as_view(),
        name="conductor-component-search",
    ),
    path(
        "account/",
        views.ConductorAccountView.as_view(),
        name="conductor-account",
    ),
    path(
        "account/password-change/",
        views.ConductorAccountPasswordChangeView.as_view(),
        name="conductor-account-password-change",
    ),
]
