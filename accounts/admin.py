from django.contrib import admin
from .models import User, AuthLog, SocialAccount


admin.site.register(User)
admin.site.register(AuthLog)
admin.site.register(SocialAccount)