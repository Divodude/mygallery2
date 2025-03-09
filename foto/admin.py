from django.contrib import admin
from foto.models import dataset,profile,user_images,clubdb

# Register your modeils here.

admin.site.register(dataset)
admin.site.register(profile)
admin.site.register(user_images)
admin.site.register(clubdb)
