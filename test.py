print(
    repr(
        """
def test_code(user_message, data):
    response = openai.api.call_api([
        openai.models.Message(
            role=openai.models.Role.SYSTEM,
            content="You are an assistant to help answer the user.",
        ),
        openai.models.Message(
            role=openai.models.Role.USER,
            content=user_message,
        ),
    ])

    return response.choices[0].message.content
"""
    )
)
