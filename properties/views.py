from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    properties = get_all_properties()

    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'price': prop.price,
            'location': prop.location,
        }
        for prop in properties 
    ]
    return JsonResponse(data, safe=False)