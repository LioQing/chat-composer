from rest_framework import serializers

from core import models


class ConductorPipelinesSerializer(serializers.ModelSerializer):
    """Serializer for the PipelinesView"""

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "name",
            "created_at",
        )


class ConductorPipelineAttributesSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineAttributesView"""

    class Meta:
        model = models.Pipeline
        fields = ("response", "state", "description")


class ConductorPipelineNewSerializer(serializers.ModelSerializer):
    """Serializer for the PipelineNewView"""

    class Meta:
        model = models.Pipeline
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("id", "name", "created_at")


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
            "function_name",
            "name",
            "arguments",
            "return_type",
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
    function_name = serializers.CharField(
        source="component.function_name", read_only=True
    )
    name = serializers.CharField(source="component.name", read_only=True)
    arguments = serializers.JSONField(
        source="component.arguments", read_only=True
    )
    return_type = serializers.CharField(
        source="component.return_type", read_only=True
    )
    description = serializers.CharField(
        source="component.description", read_only=True, allow_blank=True
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
            "arguments",
            "return_type",
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
    function_name = serializers.CharField(required=True, allow_blank=True)
    name = serializers.CharField(required=True, allow_blank=True)
    arguments = serializers.JSONField(required=True)
    return_type = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    code = serializers.CharField(required=True, allow_blank=True)
    state = serializers.JSONField(required=True)


class ConductorPipelineSaveSerializer(serializers.Serializer):
    """Serializer for the ConductorPipelineSaveView"""

    name = serializers.CharField(required=True, allow_blank=True)
    response = serializers.CharField(required=True, allow_blank=True)
    state = serializers.JSONField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    components = ConductorPipelineSaveComponentInstanceSerializer(
        many=True, required=True
    )


class ConductorPipelineDownloadSerializer(serializers.Serializer):
    """Serializer for the ConductorPipelineDownloadView"""

    pass


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


class ConductorAccountApiKeyRefreshSerializer(serializers.Serializer):
    """Serializer for the ConductorAccountApiKeyRefreshView"""

    password = serializers.CharField(required=True)
    api_key = serializers.CharField(read_only=True)


class ConductorAccountApiKeyRevealSerializer(serializers.Serializer):
    """Serializer for the ConductorAccountApiKeyRevealView"""

    password = serializers.CharField(required=True)
    api_key = serializers.CharField(read_only=True)


class ConductorChatSendSerializer(serializers.Serializer):
    """Serializer for the ConductorChatSendView"""

    user_message = serializers.CharField(required=True)
    resp_message = serializers.CharField(read_only=True)
    exit_code = serializers.IntegerField(read_only=True)


class ConductorChatHistorySerializer(serializers.ModelSerializer):
    """Serializer for the ConductorChatHistoryView"""

    class Meta:
        model = models.Chat
        fields = (
            "id",
            "user_message",
            "resp_message",
            "exit_code",
            "created_at",
        )


class ConductorChatSaveChatSerializer(serializers.Serializer):
    """Serializer for the ConductorChatSaveChatView"""

    user_message = serializers.CharField(required=True)
    resp_message = serializers.CharField(required=True)
    exit_code = serializers.IntegerField(required=True)


class ConductorChatComponentStateSerializer(serializers.ModelSerializer):
    """Serializer for the ConductorChatStatesView"""

    class Meta:
        model = models.Component
        fields = (
            "id",
            "state",
        )


class ConductorChatStatesSerializer(serializers.Serializer):
    """Serializer for the ConductorChatStatesView"""

    component_states = ConductorChatComponentStateSerializer(
        many=True, required=True
    )
    pipeline_state = serializers.JSONField(required=True)


class ConductorChatOaiChatcmplSerializer(serializers.Serializer):
    """Serializer for the ConductorChatOaiChatcmplView"""

    request = serializers.JSONField(required=True)
    response = serializers.JSONField(read_only=True)


class ConductorChatVaiGeminiProSerializer(serializers.Serializer):
    """Serializer for the ConductorChatVaiGeminiProView"""

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


class ConductorAdminTokenUsageUserSerializer(serializers.Serializer):
    """Serializer for the ConductorAdminTokenUsageView"""

    oai = serializers.IntegerField(read_only=True)
    vai = serializers.IntegerField(read_only=True)


class ConductorAdminTokenUsageSerializer(serializers.Serializer):
    """Serializer for the ConductorAdminTokenUsageView"""

    username = serializers.CharField(read_only=True)
    usage = ConductorAdminTokenUsageUserSerializer(read_only=True)
