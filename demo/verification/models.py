from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class EmailVerification(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField('Email', max_length=75)
    verification_key = models.CharField('Verification Key', max_length=255)
    issued_at = models.DateTimeField(auto_now_add=True)
    entry_valid = models.BooleanField('Valid Entry', default=True)
    attempts = models.IntegerField('Total Attempts', default=0)
    email_send = models.BooleanField('Email Send', default=False)
    email_expired_after = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email_expired_after = datetime.now()+timedelta(days=1)
        super(EmailVerification, self).save(*args, **kwargs)
