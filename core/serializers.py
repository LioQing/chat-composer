from rest_framework import serializers

from . import models


class PingPongSerializer(serializers.Serializer):
    """Serializer for the PingPongView"""

    ping = serializers.CharField(max_length=4)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""

    class Meta:
        model = models.User
        fields = "__all__"


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for the Component model"""

    class Meta:
        model = models.Component
        fields = "__all__"


class PipelineSerializer(serializers.ModelSerializer):
    """Serializer for the Pipeline model"""

    class Meta:
        model = models.Pipeline
        fields = "__all__"


class PipelineRunSerializer(serializers.Serializer):
    """Serializer for the PipelineRunView"""

    user_message = serializers.CharField(required=True)
    response = serializers.JSONField(read_only=True)


class ComponentInstanceSerializer(serializers.ModelSerializer):
    """Serializer for the ComponentInstance model"""

    class Meta:
        model = models.ComponentInstance
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    """Serializer for the Chat model"""

    class Meta:
        model = models.Chat
        fields = "__all__"
