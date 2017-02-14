from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from custom.models import Provider
from utils.response import success_response, need_login


@csrf_exempt
def get_provider(request):
    if not request.user.is_active:
        return need_login()
    result = []
    providers = Provider.objects.all()
    for item in providers:
        result.append({'id': item.id, 'name': item.name})
    return success_response(result)


def get_saler(request):
    pass
