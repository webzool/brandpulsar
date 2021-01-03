import math
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class BrandpulsarPagination(LimitOffsetPagination):
    """ Overrides LimitOffsetPagination to add max_page data
    """
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('started_from', self.offset),
            ('max_page', math.ceil(self.count / self.limit)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))