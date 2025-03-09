from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from foto import models
from foto.models import dataset,profile,user_images,clubdb
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import cv2
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from foto.face_recognition import *
from foto import face_recognition

# Create your views here.
def home(request):
    return redirect("auth")




def upload(request):
    events=set(data=dataset.objects.all().event.value())
    data=dataset.objects.filter(event_icontains="f{events}")
    return HttpResponse("hi")

    
    


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
from datetime import datetime
from .models import dataset  # Import your model
from django.db.models import Sum 

@csrf_exempt
def fetch(request):
    if request.method == "POST":
        # Handle like button click
        if "imageId" in request.POST:
            try:
                image_id = request.POST.get("imageId")
                if not image_id:
                    return JsonResponse({'success': False, 'error': 'imageId is required'}, status=400)

                # Get the image object
                image = dataset.objects.get(id=image_id)

                # Check if the user has already liked the image
                user_has_liked = request.session.get(f'liked_{image_id}', False)

                if user_has_liked:
                    # User has already liked the image, so decrement the like count
                    image.likes -= 1
                    request.session[f'liked_{image_id}'] = False  # Update session state
                else:
                    # User has not liked the image, so increment the like count
                    image.likes += 1
                    request.session[f'liked_{image_id}'] = True  # Update session state

                image.save()

                # Return the updated like count and the new like state
                return JsonResponse({
                    'success': True,
                    'likes': image.likes,
                    'liked': request.session[f'liked_{image_id}']
                })
            except dataset.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)

        elif "name" in request.POST:
            name = request.POST.get("name")
            album = request.POST.get("album")
            image = request.FILES.getlist('image')
            date = datetime.now()
            for i in image:

                db = dataset.objects.create(
                    name=name,
                    event=album,
                    date=date,
                    images=i
                )
                db.save()

            return redirect("fetch")

        elif "search" in request.POST:
            search = request.POST.get("search")
            data = dataset.objects.filter(event__icontains=search)
            events = [obj.event for obj in data]
            events = set(events)
            return render(request, "album.html", {"alb_img": data, "events": events})

    search = "Aavesh"
    like = False
    sort_feild="likes"
    data = dataset.objects.all().order_by(f"-{sort_feild}")

    count = data.count()
    event_data = dataset.objects.distinct("events")
    events = [obj.event for obj in data]
    events = set(events)
    total_likes = dataset.objects.aggregate(total_likes=Sum('likes'))['total_likes']

    return render(request, "index.html", {
        "clubs":clubdb.objects.all(),
        "user": request.user,
        "events": events,
        "data": data,
        "like": like,
        "total_photos": count,
        "total_likes": total_likes
    })



def auth(reuqest):
    
    if reuqest.method=='POST':
        email=reuqest.POST.get("email")
        password=reuqest.POST.get("password")
        try:
            user=User.objects.get(username=email)
        except:
            HttpResponse("error 404")
        user=authenticate(reuqest,username=email,password=password)
        if user is not None:
            
            login(reuqest,user)
            return redirect('fetch')
        else:
            HttpResponse("incorrect credentials")
        
    return render(reuqest,"userprofile.html")






def album(request):
    value = request.GET.get('value')
    
    dr=dataset.objects.filter(event=value)
    """reqfiles = [obj.path for obj in dr]"""
    data=dataset.objects.all()
    events=[obj.event for obj in data]
    events=set(events)

    

    return render(request,"album.html",{"alb_img":dr,"events":events, "clubs":clubdb.objects.all()})
    
def sign_up(reuqest):
    if reuqest.method=="POST":
        email=reuqest.POST.get("email")
        password=reuqest.POST.get("password")

        
        user=User.objects.filter(username=email)
        if user.exists():
            HttpResponse("user exist")
        user=User.objects.create_user(username=email)
        
        user.set_password(password)
        user.save()
        profile.objects.create(user=user)
        
        redirect("auth")

        
        
    return render(reuqest,"sign_up.html")

from mygallery import settings


import os
from django.conf import settings

import os
from django.conf import settings

def ai_photos(request):
    media_path = settings.MEDIA_ROOT
    profile_inst=profile.objects.get(user=request.user)
    a=int(profile_inst.user.id)
    
    target_path=f"embedding\{a}.pkl"
    if os.path.exists(target_path):
    
        absolute_image_files = face_recognition.find_matching_images(target_dir=target_path, main_dir="main.pkl")
        relative_image_files = [os.path.relpath(img_path, media_path) for img_path in absolute_image_files]
        print(relative_image_files)
        image_urls = [f"{settings.MEDIA_URL}{img}" for img in relative_image_files]
        return render(request, "ai.html", {'urls': image_urls,"total_photos":len(image_urls)})
    else:
        return redirect("generate")
    





from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
def generate_embedding(request):
    inst_=profile.objects.get(user=request.user)
    
    if request.method == "POST":
        uploaded_files = ["image1", "image2", "image3", "image4", "image5"]   
        for image_key in uploaded_files:
            image_file = request.FILES.get(image_key)  
            if image_file:
                image_instance = user_images.objects.create(image=image_file)
                image_instance.user.add(inst_) 
                print(f"Uploaded: {image_key}")     
        paths=[]
        images=user_images.objects.filter(user=inst_)
        for image in images:
            paths.append(image.image.path)
        
        x=inst_.user.id
        face_recognition.get_embeddings_from_dir(embd_save_path=f"embedding\{x}.pkl", image_paths=paths)


    
    return render(request, "generate_embedding.html") 

        
            
#import schedule






#schedule.every().day.at("23:55").do(face_recognition.run_midnight_embedding_extraction)