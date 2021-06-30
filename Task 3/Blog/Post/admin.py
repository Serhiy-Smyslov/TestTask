from django.contrib import admin
from . import models


admin.site.register(models.SimpleUser)
admin.site.register(models.UserPost)
admin.site.register(models.Comment)
