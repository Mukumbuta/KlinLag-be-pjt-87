from django.contrib import admin

 
from .models import *
# Register your models here.
admin.site.register(PickupTime)
admin.site.register(Profile)
admin.site.register(Blogpost)
admin.site.register(Comment)
admin.site.register(Schedule)
admin.site.register(Waste)
admin.site.register(PickupRequest)
