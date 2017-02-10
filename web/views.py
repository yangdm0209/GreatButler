from django.shortcuts import render, render_to_response


# Create your views here.
from django.template import RequestContext


def index(request):
    pass


def login(request):
    if request.method == 'GET':
        return render_to_response('login.html',RequestContext(request, {'user': 'Kevin'}))


def logout(request):
    pass
