from django.urls import path,include
from foto.api import views

urlpatterns = [
    path("data/",views.api)
]
