from django.shortcuts import render

# Create your views here.
from product.models import Product
from utils.response import need_login, success_response


def get_products(request):
    if not request.user.is_active:
        return need_login()
    products = []
    for p in Product.objects.all().order_by('name'):
        products.append({'id': p.id, 'name': p.name, 'price': p.price_retail, 'cost': p.price_cost})
    return success_response(products)
