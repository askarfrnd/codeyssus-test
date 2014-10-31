from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    REGISTRATION_TYPE = (
        ('NORMAL', 'NORMAL'),
        ('SOCIAL', 'SOCIAL'),
    )

    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    registration_type = models.CharField(max_length=10, choices=REGISTRATION_TYPE, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name