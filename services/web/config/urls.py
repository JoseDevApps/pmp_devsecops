from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def health(request):
    return JsonResponse({"status": "ok", "service": "web"})


urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
]
