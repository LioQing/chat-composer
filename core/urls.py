from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"model/user", views.UserView)
router.register(r"model/component", views.ComponentView)
router.register(r"model/pipeline", views.PipelineView)
router.register(r"model/component-instance", views.ComponentInstanceView)

urlpatterns = [
    *router.urls,
    path("ping", views.PingPongView.as_view(), name="ping"),
]
