from django.core.paginator import Paginator

from .constants import RESTRICTION_LISTS


def paginator(request, obj):
    page_obj = Paginator(obj, RESTRICTION_LISTS)
    page_number = request.GET.get('page')
    return page_obj.get_page(page_number)
