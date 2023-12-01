from rest_framework import serializers

from core import models


class ConductorPipelineSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineView"""

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "name",
            "is_safe",
            "created_at",
        )


class ConductorPipelineStateSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineStateView"""

    class Meta:
        model = models.Pipeline
        fields = ("state",)


class ConductorPipelineNewSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineNewView"""

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "name",
            "is_safe",
            "created_at",
        )
        read_only_fields = ("id", "name", "is_safe", "created_at")


class ConductorPipelineDeleteSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineDeleteView"""

    pass


class ConductorPipelineRenameSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineRenameView"""

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class ConductorComponentSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorComponentView"""

    class Meta:
        model = models.Component
        fields = (
            "id",
            "name",
            "function_name",
            "description",
            "code",
            "state",
            "is_template",
            "created_at",
        )


class ConductorPipelineComponentInstanceSerializer(
    serializers.ModelSerializer
):
    """Serializer for the ConductorPipelineComponentInstanceView"""

    component_id = serializers.IntegerField(
        source="component.id", read_only=True
    )
    name = serializers.CharField(source="component.name", read_only=True)
    function_name = serializers.CharField(
        source="component.function_name", read_only=True
    )
    description = serializers.JSONField(
        source="component.description", read_only=True
    )
    code = serializers.CharField(source="component.code", read_only=True)
    state = serializers.JSONField(source="component.state", read_only=True)
    is_template = serializers.BooleanField(
        source="component.is_template", read_only=True
    )
    created_at = serializers.DateTimeField(
        source="component.created_at", read_only=True
    )

    class Meta:
        model = models.ComponentInstance
        fields = (
            "id",
            "order",
            "is_enabled",
            "component_id",
            "name",
            "function_name",
            "description",
            "code",
            "state",
            "is_template",
            "created_at",
        )
        read_only_fields = (
            "id",
            "order",
            "is_enabled",
        )


class ConductorPipelineComponentInstanceNewSerializer(
    ConductorPipelineComponentInstanceSerializer
):
    """Serializer for the ConductorPipelineComponentInstanceNewView"""

    template_component_id = serializers.IntegerField(required=False)

    class Meta:
        model = models.ComponentInstance
        fields = ConductorPipelineComponentInstanceSerializer.Meta.fields + (
            "template_component_id",
        )
        read_only_fields = (
            ConductorPipelineComponentInstanceSerializer.Meta.read_only_fields
        )


class ConductorPipelineComponentInstanceDeleteSerializer(
    serializers.Serializer
):
    """Serializer for the ConductorPipelineComponentInstanceDeleteView"""

    pass


class ConductorComponentSearchSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorComponentSearchView"""

    class Meta:
        model = models.Component
        fields = (
            "id",
            "name",
        )


class ConductorPipelineSaveComponentInstanceSerializer(serializers.Serializer):
    """Serializer for the ConductorPipelineSaveSerializer"""

    id = serializers.IntegerField(required=True)
    order = serializers.IntegerField(required=True)
    is_enabled = serializers.BooleanField(required=True)
    name = serializers.CharField(required=True)
    function_name = serializers.CharField(required=True)
    description = serializers.JSONField(required=True)
    code = serializers.CharField(required=True)
    state = serializers.JSONField(required=True)


class ConductorPipelineSaveSerializer(serializers.Serializer):
    """Serializer for the ConductorPipelineSaveView"""

    name = serializers.CharField(required=True)
    state = serializers.JSONField(required=True)
    components = ConductorPipelineSaveComponentInstanceSerializer(
        many=True, required=True
    )


class ConductorAccountSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorAccountView"""

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "is_whitelisted",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "username",
            "name",
            "email",
            "is_whitelisted",
            "date_joined",
        )


class ConductorAccountPasswordChangeSerializer(serializers.Serializer):
    """Serializer for the ConductorAccountPasswordChangeView"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ConductorChatSendSerializer(serializers.Serializer):
    """Serializer for the ConductorChatSendView"""

    user_message = serializers.CharField(required=True)
    api_message = serializers.CharField(read_only=True)


class ConductorChatHistorySerializer(serializers.ModelSerializer):
    """Serializer for the ConductorChatHistoryView"""

    class Meta:
        model = models.Chat
        fields = (
            "id",
            "user_message",
            "api_message",
            "created_at",
        )


class ConductorChatComponentSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorChatPipelineView"""

    class Meta:
        model = models.Component
        fields = (
            "id",
            "name",
            "code",
            "function_name",
            "state",
        )


class ConductorChatPipelineSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorChatPipelineView"""

    components = ConductorChatComponentSerializer(
        many=True, source="get_components"
    )

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "state",
            "components",
        )


class ConductorChatSaveChatSerializer(serializers.Serializer):
    """Serializer for the ConductorChatSaveChatView"""

    user_message = serializers.CharField(required=True)
    api_message = serializers.CharField(required=True)


class ConductorChatSaveStatesSerializer(serializers.Serializer):
    """Serializer for the ConductorChatSaveStatesView"""

    state = serializers.JSONField(required=True)
    pstate = serializers.JSONField(required=True)


class ConductorChatOaiChatcmplSerializer(serializers.Serializer):
    """Serializer for the ConductorChatOaiChatcmplView"""

    request = serializers.JSONField(required=True)
    response = serializers.JSONField(read_only=True)


class ConductorAdminWhitelistSerializer(serializers.Serializer):
    """Serializer for the ConductorAdminWhitelistView"""

    username = serializers.CharField(required=True)
    whitelist = serializers.BooleanField(default=True)


class ConductorAdminCreateUserSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorAdminCreateUserView"""

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "password",
        )
        read_only_fields = ("id", "password")


class ConductorAdminMakeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorAdminMakeTemplateView"""

    class Meta:
        model = models.Component
        fields = ("is_template",)


class ConductorAdminMakeSafeSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorAdminMakeSafeView"""

    class Meta:
        model = models.Pipeline
        fields = ("is_safe",)
