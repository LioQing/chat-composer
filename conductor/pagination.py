from rest_framework import pagination, response


class ChatPagination(pagination.PageNumberPagination):
    """Pagination for the Chat model"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        """Return the paginated response"""
        return response.Response(data=data)
