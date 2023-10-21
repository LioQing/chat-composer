from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"model/user", views.UserView)
router.register(r"model/component", views.ComponentView)
router.register(r"model/pipeline", views.PipelineView)
router.register(r"model/pipeline-component", views.PipelineComponentView)

run_urlpatterns = [
    path(
        "pipeline/run/<int:id>/",
        views.PipelineRunView.as_view(),
        name="pipeline-run",
    ),
]

admin_action_urlpatterns = [
    path(
        "user/whitelist/",
        views.UserWhitelistView.as_view(),
        name="user-whitelist",
    ),
]

urlpatterns = [
    *router.urls,
    *run_urlpatterns,
    *admin_action_urlpatterns,
    path("ping", views.PingPongView.as_view(), name="ping"),
]
