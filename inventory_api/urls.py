from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from entities import api as entities_api

api = NinjaAPI()
api.add_router("", entities_api.router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]