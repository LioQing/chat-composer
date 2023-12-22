from django.urls import path, register_converter
from rest_framework import routers

from engine.containment import ContainmentArchiveType

from . import views


class ArchiveTypeConverter:
    """Archive type converter class"""

    regex = r"(zip|targz)"

    def to_python(self, value: str) -> ContainmentArchiveType:
        """Convert to python"""
        if value == "zip":
            return ContainmentArchiveType.ZIP
        elif value == "targz":
            return ContainmentArchiveType.TARGZ
        else:
            raise ValueError("Invalid archive type")

    def to_url(self, value: ContainmentArchiveType) -> str:
        """Convert to url"""
        if value == ContainmentArchiveType.ZIP:
            return "zip"
        elif value == ContainmentArchiveType.TARGZ:
            return "targz"


register_converter(ArchiveTypeConverter, "archive")

router = routers.SimpleRouter()
router.register(r"pipelines", views.ConductorPipelinesView)
router.register(r"pipeline/attributes", views.ConductorPipelineAttributesView)
router.register(r"pipeline/new", views.ConductorPipelineNewView)
router.register(r"pipeline/delete", views.ConductorPipelineDeleteView)
router.register(r"pipeline/rename", views.ConductorPipelineRenameView)
router.register(
    r"component/details",
    views.ConductorComponentDetailsView,
)
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
    r"chat/history/(?P<pk>\d+)",
    views.ConductorChatHistoryView,
)
router.register(
    r"admin/create-user",
    views.ConductorAdminCreateUserView,
)
router.register(
    r"admin/make-template",
    views.ConductorAdminMakeTemplateView,
)

urlpatterns = [
    *router.urls,
    path(
        "component/search/",
        views.ConductorComponentSearchView.as_view(),
        name="conductor-component-search",
    ),
    path(
        "pipeline/save/<int:pk>/",
        views.ConductorPipelineSaveView.as_view(),
        name="conductor-pipeline-save",
    ),
    path(
        "pipeline/download/<int:pk>/<archive:archive_type>/",
        views.ConductorPipelineDownloadView.as_view(),
        name="conductor-pipeline-download",
    ),
    path(
        "chat/send/<int:pk>/",
        views.ConductorChatSendView.as_view(),
        name="conductor-chat-send",
    ),
    path(
        "chat/save/chat/<int:pk>/",
        views.ConductorChatSaveChatView.as_view(),
        name="conductor-chat-save-chat",
    ),
    path(
        "chat/states/<int:pk>/",
        views.ConductorChatStatesView.as_view(),
        name="conductor-chat-states",
    ),
    path(
        "chat/oai/chatcmpl/<int:pk>/",
        views.ConductorChatOaiChatcmplView.as_view(),
        name="conductor-chat-oai-chatcmpl",
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
    path(
        "account/api-key/refresh/",
        views.ConductorAccountApiKeyRefreshView.as_view(),
        name="conductor-account-api-key-refresh",
    ),
    path(
        "account/api-key/reveal/",
        views.ConductorAccountApiKeyRevealView.as_view(),
        name="conductor-account-api-key-reveal",
    ),
    path(
        "admin/whitelist/",
        views.ConductorAdminWhitelistView.as_view(),
        name="conductor-admin-whitelist",
    ),
]
