import json
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.http import JsonResponse


def users(request, *args, **kwargs):
    data = {}
    model = get_user_model()
    resource = kwargs.get("id", None)
    body = json.loads(request.body) if request.body else None
    status = 200
    if request.method == "GET":
        queryset = (
            model.objects.filter(pk=resource) if resource else model.objects.all()
        )
        status = 200
    if request.method == "DELETE" and resource:
        model.objects.get(id=resource).delete()
        queryset = []
        status = 200
    if request.method in ("POST", "PUT") and not resource:
        queryset.create(**body)
        status = 201
    if request.method in ("POST", "PATCH", "PUT") and resource:
        model.objects.filter(id=resource).update(**body)
        queryset = model.objects.filter(id=resource)
        status = 200

    results = json.loads(serialize("json", queryset))
    data = {"results": results}
    return JsonResponse(data, status=status)
