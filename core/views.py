from rest_framework import (
    exceptions,
    generics,
    permissions,
    response,
    views,
    viewsets,
)

from . import models, serializers


class PingPongView(views.APIView):
    """View for checking if the server is running"""

    serializer_class = serializers.PingPongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return a pong response"""
        serializer = self.serializer_class(data={"ping": "pong"})
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)


class UserView(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the User model"""

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer: serializers.UserSerializer):
        """Create the user"""
        user: models.User = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer: serializers.UserSerializer):
        """Update the user"""
        user: models.User = serializer.save()

        if serializer.validated_data.get("password"):
            user.set_password(user.password)
            user.save()


class ComponentView(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the Component model"""

    queryset = models.Component.objects.all()
    serializer_class = serializers.ComponentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Return the queryset"""
        if self.request.user.is_superuser or self.request.method == "GET":
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create the component"""
        user: models.User = serializer.validated_data["user"]
        if not user.is_superuser and user != self.request.user:
            raise exceptions.PermissionDenied(
                "You do not have permission to create a component for other"
                " user"
            )
        serializer.save()


class PipelineView(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the Pipeline model"""

    queryset = models.Pipeline.all_objects.all()
    serializer_class = serializers.PipelineSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Return the queryset"""
        if self.request.user.is_superuser or self.request.method == "GET":
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create the pipeline"""
        user: models.User = serializer.validated_data["user"]
        if not user.is_superuser and user != self.request.user:
            raise exceptions.PermissionDenied(
                "You do not have permission to create a pipeline for other"
                " user"
            )
        serializer.save()


class ComponentInstanceView(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the ComponentInstance model"""

    queryset = models.ComponentInstance.objects.all()
    serializer_class = serializers.ComponentInstanceSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Return the queryset"""
        if self.request.user.is_superuser or self.request.method == "GET":
            return self.queryset

        return self.queryset.filter(pipeline__user=self.request.user)

    def perform_create(self, serializer):
        """Create the pipeline component"""
        user: models.User = serializer.validated_data["pipeline"].user
        if not user.is_superuser and user != self.request.user:
            raise exceptions.PermissionDenied(
                "You do not have permission to create a pipeline component for"
                " other user"
            )
        serializer.save()


class ChatView(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
    viewsets.GenericViewSet,
):
    """Viewset for the Chat model"""

    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Return the queryset"""
        if self.request.user.is_superuser or self.request.method == "GET":
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create the chat"""
        user: models.User = serializer.validated_data["pipeline"].user
        if not user.is_superuser and user != self.request.user:
            raise exceptions.PermissionDenied(
                "You do not have permission to create a chat for other user's"
                " pipeline"
            )
        serializer.save()
