import json

from django.http import HttpResponse



def test_cors(request):
    return HttpResponse('hahaha')


