from django.contrib import admin
from .models import item,PlayerProfile,UserItem,FishingSession

# Register your models here.
admin.site.register(item)
admin.site.register(PlayerProfile)
admin.site.register(UserItem)
admin.site.register(FishingSession)