from django.db.models import Q
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, views, viewsets

from core import models
from rest_auth import permissions

from . import exceptions, serializers


class ConductorPipelineView(
    generics.ListAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the pipeline list"""

    queryset = models.Pipeline.objects.all()
    serializer_class = serializers.ConductorPipelineSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get_queryset(self):
        """Return the pipelines owned by the user"""
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

    def perform_destroy(self, instance: models.Pipeline):
        """Set the pipeline as inactive"""
        instance.is_active = False
        instance.save()

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
                name=template_component.name,
                function_name=template_component.function_name,
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
        serializer.validated_data["name"] = component.name
        serializer.validated_data["function_name"] = component.function_name
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
        instance.is_active = False
        instance.save()

        # Reorder the component instances
        for (
            component_instance
        ) in instance.pipeline.componentinstance_set.all():
            if component_instance.order > instance.order:
                component_instance.order -= 1
                component_instance.save()

    def get_queryset(self):
        """Return the component instances owned by the user"""
        return self.queryset.filter(pipeline__user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name="query", type=str),
            OpenApiParameter(name="filter", type=str),
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


class ConductorAccountView(
    views.APIView,
):
    """View to get the user's account information"""

    serializer_class = serializers.ConductorAccountSerializer
    permission_classes = [permissions.IsWhitelisted]

    def get(self, request: views.Request, *args, **kwargs):
        """Return the user's account information"""
        user = models.User.objects.get(id=request.user.id)
        serializer = self.serializer_class(
            data={
                "id": user.id,
                "username": user.username,
                "name": user.first_name + " " + user.last_name,
                "email": user.email,
                "is_whitelisted": user.is_whitelisted,
                "date_joined": user.date_joined,
            }
        )

        serializer.is_valid(raise_exception=True)
        return views.Response(serializer.data)


class ConductorAccountPasswordChangeView(
    views.APIView,
):
    """View to change the user's password"""

    serializer_class = serializers.ConductorAccountPasswordChangeSerializer
    permission_classes = [permissions.IsWhitelisted]

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
