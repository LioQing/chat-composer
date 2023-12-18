from django.urls import path
from rest_framework import routers

from . import views

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
