from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Tasks)
admin.site.register(Invitation)
admin.site.register(SocialMedia)
admin.site.register(Blum)