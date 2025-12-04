import json
from django.http import HttpRequest


def parse_request_data(request: HttpRequest) -> dict:
    if request.method == "POST":
        try:
            return json.loads(request.body)  # JSON
        except Exception:
            return request.POST.dict()       # form-data

    elif request.method == "GET":
        return request.GET.dict()

    return {}
