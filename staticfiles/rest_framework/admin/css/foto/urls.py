
from django.contrib import admin
from django.urls import path,include
from foto import views
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('papa/',admin.site.urls),
    path('',views.home,name="home"),
    path("upload/",views.upload,name="upload"),
    path("fetch/",views.fetch,name="fetch"),
    path("auth/",views.auth,name="auth"),
    path("album/",views.album,name="album"),
    path("sign_up/",views.sign_up,name="sign_up"),
    path("ai_photos",views.ai_photos,name="ai_photos"),
    path("generate/",views.generate_embedding,name="generate")  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)