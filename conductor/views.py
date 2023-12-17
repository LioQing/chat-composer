import logging

from django.db.models import Q
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from pydantic import ValidationError
from rest_framework import generics
from rest_framework import permissions as rest_permissions
from rest_framework import views, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

import engine.modules.oai
from core import models
from engine.containment import containment
from rest_auth import permissions

from . import exceptions, pagination, serializers


class ConductorPipelinesView(
    generics.ListAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the pipeline list"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelinesSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the pipelines owned by the user"""
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)


class ConductorPipelineAttributesView(
    generics.RetrieveAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for retrieving a pipeline's attributes"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineAttributesSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the pipelines owned by the user"""
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)


class ConductorPipelineNewView(
    generics.CreateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for creating a new pipeline"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineNewSerializer
    permission_classes = [permissions.IsWhitelisted]

    def perform_create(
        self, serializer: serializers.ConductorPipelineNewSerializer
    ):
        """Create a new pipeline"""
        serializer.save(user=self.request.user)


class ConductorPipelineDeleteView(
    generics.DestroyAPIView,
    viewsets.GenericViewSet,
):
    """View to set a pipeline as inactive"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineDeleteSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the pipelines owned by the user"""
        return self.queryset.filter(user=self.request.user)


class ConductorPipelineRenameView(
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """View to rename a pipeline"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineRenameSerializer
    permission_classes = [permissions.IsWhitelisted]
    http_method_names = ["patch"]

    def perform_update(
        self, serializer: serializers.ConductorPipelineRenameSerializer
    ):
        """Rename the pipeline"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return the pipelines owned by the user"""
        return self.queryset.filter(user=self.request.user)


class ConductorComponentDetailsView(
    generics.RetrieveAPIView,
    viewsets.GenericViewSet,
):
    """View to get a component's details"""

    queryset = models.Component.objects.all()
    serializer_class = serializers.ConductorComponentSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the components owned by the user or is a template"""
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(
            Q(user=self.request.user) | Q(is_template=True)
        )


class ConductorPipelineComponentInstanceView(
    generics.RetrieveAPIView,
    viewsets.GenericViewSet,
):
    """View to get pipeline's component instances"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineComponentInstanceSerializer
    permission_classes = [permissions.IsWhitelisted]

    def retrieve(self, request: views.Request, *args, **kwargs):
        """Return the pipeline's component instances"""
        pipeline = self.get_object()
        serializer = self.serializer_class(
            pipeline.componentinstance_set.all().order_by("order"), many=True
        )
        return views.Response(serializer.data)

    def get_queryset(self):
        """Return the pipelines owned by the user"""
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)


class ConductorPipelineComponentInstanceNewView(
    generics.CreateAPIView,
    viewsets.GenericViewSet,
):
    """View to create a new component instance"""

    queryset = models.ComponentInstance.objects.all()
    serializer_class = (
        serializers.ConductorPipelineComponentInstanceNewSerializer
    )
    permission_classes = [permissions.IsWhitelisted]

    def perform_create(
        self,
        serializer: serializer_class,
    ):
        """Create a new component instance"""
        pipeline = models.Pipeline.objects.get(id=self.kwargs["pk"])
        order = pipeline.componentinstance_set.count()

        # Duplicate the template component
        if serializer.validated_data.get("template_component_id"):
            template_component = models.Component.objects.get(
                id=serializer.validated_data["template_component_id"]
            )
            component = models.Component.objects.create(
                user=self.request.user,
                function_name=template_component.function_name,
                name=template_component.name,
                arguments=template_component.arguments,
                return_type=template_component.return_type,
                description=template_component.description,
                code=template_component.code,
                state=template_component.state,
            )
        else:
            component = models.Component.objects.create(
                user=self.request.user,
                name=f"Component {order}",
                function_name=f"component_{order}",
            )

        # Create the component instance
        component_instance = models.ComponentInstance.objects.create(
            pipeline=pipeline,
            component=component,
            order=order,
            is_enabled=True,
        )

        # Fill serializer with component instance data
        serializer.instance = component_instance
        serializer.validated_data["component_id"] = component.id
        serializer.validated_data["function_name"] = component.function_name
        serializer.validated_data["name"] = component.name
        serializer.validated_data["arguments"] = component.arguments
        serializer.validated_data["return_type"] = component.return_type
        serializer.validated_data["description"] = component.description
        serializer.validated_data["code"] = component.code
        serializer.validated_data["state"] = component.state
        serializer.validated_data["is_template"] = component.is_template
        serializer.validated_data["created_at"] = component.created_at

        serializer.save()


class ConductorPipelineComponentInstanceDeleteView(
    generics.DestroyAPIView,
    viewsets.GenericViewSet,
):
    """View to set a component instance as inactive"""

    queryset = models.ComponentInstance.objects.all()
    serializer_class = (
        serializers.ConductorPipelineComponentInstanceDeleteSerializer
    )
    permission_classes = [permissions.IsWhitelisted]

    def perform_destroy(self, instance: models.ComponentInstance):
        """Set the component instance as inactive"""
        # Reorder the component instances
        for (
            component_instance
        ) in instance.pipeline.componentinstance_set.all():
            if component_instance.order > instance.order:
                component_instance.order -= 1
                component_instance.save()

        # Delete the component instance
        instance.delete()

    def get_queryset(self):
        """Return the component instances owned by the user"""
        return self.queryset.filter(pipeline__user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name="query", type=str),
            OpenApiParameter(
                name="filter", type=str, enum=("templates", "created")
            ),
        ]
    )
)
class ConductorComponentSearchView(views.APIView):
    """View to search for components"""

    serializer_class = serializers.ConductorComponentSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get(self, request: views.Request, *args, **kwargs):
        """Return the components that match the search query"""
        query = request.query_params.get("query", "")
        filter = request.query_params.get("filter", "")

        filter_dict = {}
        filter_dict["is_template"] = filter == "templates"
        if filter == "created":
            filter_dict["user"] = request.user

        components = models.Component.objects.filter(
            name__icontains=query, **filter_dict
        )
        serializer = self.serializer_class(components, many=True)
        return views.Response(serializer.data)


class ConductorPipelineSaveView(views.APIView):
    """View to save pipeline"""

    serializer_class = serializers.ConductorPipelineSaveSerializer
    permission_classes = [permissions.IsWhitelisted]

    def patch(self, request: views.Request, pk: int, *args, **kwargs):
        """Save the pipeline"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pipeline = models.Pipeline.objects.filter(user=request.user).get(id=pk)

        # Save the pipeline attributes
        pipeline.name = serializer.validated_data["name"]
        pipeline.response = serializer.validated_data["response"]
        pipeline.state = serializer.validated_data["state"]
        pipeline.description = serializer.validated_data["description"]
        pipeline.save()

        # For each component, save them
        for component in serializer.validated_data["components"]:
            component_instance = models.ComponentInstance.objects.get(
                id=component["id"]
            )
            component_instance.order = component["order"]
            component_instance.is_enabled = component["is_enabled"]
            component_instance.save()

            component_instance.component.function_name = component[
                "function_name"
            ]
            component_instance.component.name = component["name"]
            component_instance.component.arguments = component["arguments"]
            component_instance.component.return_type = component["return_type"]
            component_instance.component.description = component["description"]
            component_instance.component.code = component["code"]
            component_instance.component.state = component["state"]
            component_instance.component.save()

        return views.Response(serializer.data)


class ConductorAccountView(
    views.APIView,
):
    """View to get the user's account information"""

    serializer_class = serializers.ConductorAccountSerializer
    permission_classes = [rest_permissions.IsAuthenticated]

    def get(self, request: views.Request, *args, **kwargs):
        """Return the user's account information"""
        user = models.User.objects.get(id=request.user.id)
        serializer = self.serializer_class(user)
        return views.Response(serializer.data)


class ConductorAccountPasswordChangeView(
    views.APIView,
):
    """View to change the user's password"""

    serializer_class = serializers.ConductorAccountPasswordChangeSerializer
    permission_classes = [rest_permissions.IsAuthenticated]

    def patch(self, request: views.Request, *args, **kwargs):
        """Change the user's password"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        user = models.User.objects.get(id=request.user.id)
        if not user.check_password(old_password):
            raise exceptions.IncorrectOldPasswordException()

        user.set_password(new_password)
        user.save()

        return views.Response()


class ConductorChatSendView(
    views.APIView,
):
    """View to run the chat of a pipeline"""

    serializer_class = serializers.ConductorChatSendSerializer
    permission_classes = [permissions.IsWhitelisted]

    def post(self, request: views.Request, pk: int, *args, **kwargs):
        """Run the chat"""
        serializer: serializers.ConductorChatSendSerializer = (
            self.serializer_class(data=request.data)
        )
        serializer.is_valid(raise_exception=True)
        user_message: str = serializer.validated_data["user_message"]

        pipeline: models.Pipeline = models.Pipeline.objects.filter(
            user=request.user
        ).get(id=pk)

        refresh: RefreshToken = RefreshToken.for_user(request.user)
        containment.run_pipeline(pipeline, user_message, refresh)

        return views.Response(serializer.data)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name="page", type=int),
            OpenApiParameter(name="page_size", type=int),
        ]
    )
)
class ConductorChatHistoryView(
    generics.ListAPIView,
    viewsets.GenericViewSet,
):
    """View to get the chat history of a pipeline"""

    queryset = models.Chat.objects.all()
    serializer_class = serializers.ConductorChatHistorySerializer
    pagination_class = pagination.ChatPagination
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the chat history of the pipeline"""
        q = Q()
        if not self.request.user.is_staff:
            q &= Q(pipeline__user=self.request.user)
        pipeline = models.Pipeline.objects.filter(q).get(id=self.kwargs["pk"])
        return self.queryset.filter(pipeline=pipeline).order_by("-created_at")

    def list(self, request: views.Request, *args, **kwargs):
        """Return the chat history of the pipeline"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class ConductorChatSaveChatView(views.APIView):
    """View to save chat"""

    serializer_class = serializers.ConductorChatSaveChatSerializer
    permission_classes = [permissions.IsWhitelisted]

    def patch(self, request: views.Request, pk: int, *args, **kwargs):
        """Save the chat"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pipeline = models.Pipeline.objects.filter(user=request.user).get(id=pk)

        # Save the chat
        models.Chat.objects.create(
            pipeline=pipeline,
            user_message=serializer.validated_data["user_message"],
            resp_message=serializer.validated_data["resp_message"],
            exit_code=serializer.validated_data["exit_code"],
        )

        return views.Response(serializer.data)


class ConductorChatStatesView(views.APIView):
    """View to get the chat states"""

    serializer_class = serializers.ConductorChatStatesSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get(self, request: views.Request, pk: int, *args, **kwargs):
        """Return the chat states"""
        pipeline = models.Pipeline.objects.filter(user=request.user).get(id=pk)

        serializer = self.serializer_class(
            {
                "component_states": pipeline.get_components(),
                "pipeline_state": pipeline.state,
            }
        )
        return views.Response(serializer.data)

    def post(self, request: views.Request, pk: int, *args, **kwargs):
        """Return the chat states"""
        pipeline = models.Pipeline.objects.filter(user=request.user).get(id=pk)
        components = pipeline.get_components()

        component_states = request.data["component_states"]
        pipeline_state = request.data["pipeline_state"]

        for component_state in component_states:
            component = components.get(id=component_state["id"])
            component.state = component_state["state"]
            component.save()

        pipeline.state = pipeline_state
        pipeline.save()

        return views.Response()


class ConductorChatOaiChatcmplView(views.APIView):
    """View to call the OpenAI chat completion"""

    serializer_class = serializers.ConductorChatOaiChatcmplSerializer
    permission_classes = [permissions.IsWhitelisted]

    def post(self, request: views.Request, pk: int, *args, **kwargs):
        """Call the OpenAI chat completion"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        component = models.Component.objects.filter(user=request.user).get(
            id=pk
        )

        response = None
        with engine.modules.composer.init_component(component.id):
            try:
                request_args = serializer.validated_data["request"]
                chatcmpl_request = engine.modules.oai.api.ChatcmplRequest(
                    **request_args
                )
            except ValidationError as e:
                raise exceptions.BadArgumentsException(str(e))

            response = engine.modules.oai.api.chatcmpl(chatcmpl_request)

        if response is None:
            raise ValueError("response is None")

        serializer.validated_data["response"] = response.model_dump()
        return views.Response(serializer.data)


class ConductorAdminWhitelistView(views.APIView):
    """View for whitelisting a user"""

    serializer_class = serializers.ConductorAdminWhitelistSerializer
    permission_classes = [rest_permissions.IsAdminUser]

    def patch(self, request: views.Request, *args, **kwargs):
        """Whitelist the user"""
        try:
            serializer: serializers.ConductorAdminWhitelistSerializer = (
                self.serializer_class(data=request.data)
            )
            serializer.is_valid(raise_exception=True)
            username: str = serializer.validated_data["username"]
            whitelist: bool = serializer.validated_data["whitelist"]

            user = models.User.objects.get(username=username)
            user.is_whitelisted = whitelist
            user.save()
            return views.Response(serializer.data)
        except Exception as e:
            import traceback

            traceback.print_exc()
            logger = logging.getLogger(__name__)
            logger.error(e)
            raise e


class ConductorAdminCreateUserView(
    viewsets.GenericViewSet,
):
    """View for creating a user"""

    queryset = models.User.objects.all()
    serializer_class = serializers.ConductorAdminCreateUserSerializer
    permission_classes = [rest_permissions.IsAdminUser]

    def create(self, request: views.Request, *args, **kwargs):
        """Create a user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = models.User.objects.make_random_password()
        user: models.User = serializer.save(password=password)
        user.set_password(password)
        user.save()

        data = serializer.data
        data["password"] = password
        return views.Response(
            data,
            status=views.status.HTTP_201_CREATED,
        )


class ConductorAdminMakeTemplateView(
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """View for making a component a template"""

    queryset = models.Component.objects.all()
    serializer_class = serializers.ConductorAdminMakeTemplateSerializer
    permission_classes = [rest_permissions.IsAdminUser]
    http_method_names = ["patch"]
