from django.http import JsonResponse, Http404
from django.views import View
from django.shortcuts import get_object_or_404
import json
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ItemView(View):
    def get(self, request, *args, **kwargs):
        item_id = request.GET.get("id")
        if item_id:
            try:
                item = get_object_or_404(Item, id=item_id)
                return JsonResponse({"id": item.id, "name": item.name, "description": item.description})
            except Http404:
                return JsonResponse({"error": "Item Not Found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            items = Item.objects.all().values("id", "name", "description")
            return JsonResponse(list(items), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item = Item.objects.create(
                name=data["name"], description=data["description"])
            return JsonResponse({"id": item.id, "message": "Item created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Item, id=data["id"])
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Item, id=data["id"])

            item.name = data.get("name", item.name)
            item.description = data.get("description", item.description)

            item.save()
            return JsonResponse({"message": "Item updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
