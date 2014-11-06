from django.contrib import admin

from user_profiles.models import UserProfile, Photo, Audio, Video

admin.site.register(UserProfile)
admin.site.register(Photo)
admin.site.register(Audio)
admin.site.register(Video)