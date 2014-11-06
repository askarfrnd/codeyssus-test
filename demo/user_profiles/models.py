from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" %(uuid.uuid4(), ext)
        upload_path = 'uploads/'+str(instance.user_profile.user.username)+'/'+str(instance.__class__.__name__).lower()
        return os.path.join(upload_path, filename)


class UserProfile(models.Model):
    REGISTRATION_TYPE = (
        ('NORMAL', 'NORMAL'),
        ('SOCIAL', 'SOCIAL'),
    )

    user = models.OneToOneField(User, related_name='user_profile')
    name = models.CharField(max_length=255)
    registration_type = models.CharField(max_length=10, choices=REGISTRATION_TYPE, default="SOCIAL", null=True)
    caption = models.CharField(max_length=100, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ContentBase(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    timestamp_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Photo(ContentBase):
    file_path = models.ImageField(upload_to=get_file_path, blank=True, null=True)

    def __unicode__(self):
        return self.user_profile.name


class Audio(ContentBase):
    file_path = models.FileField(upload_to=get_file_path, null=True, blank=True)

    def __unicode__(self):
        return self.user_profile.name


class Video(ContentBase):
    file_path = models.FileField(upload_to=get_file_path, null=True, blank=True)

    def __unicode__(self):
        return self.user_profile.name