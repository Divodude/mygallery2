from django.shortcuts import render,HttpResponse
from foto.models import dataset
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework import status
from rest_framework.response import Response
from foto.api.serializers import mySerializer



@api_view(["GET","POST"])
def api( request):
    if request.method=="POST":
         obj=mySerializer(data=request.data)
         if obj.is_valid():
              obj.save()
              return Response(obj.data, status=status.HTTP_201_CREATED)
         return Response(obj.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Send a POST request to create a comment"}, status=status.HTTP_200_OK)
   
    
