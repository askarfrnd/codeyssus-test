from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail

from .models import EmailVerification
from demo.settings import EMAIL_HOST_USER
from user_profiles.models import UserProfile

chars = 'abcdefghijklmnopqrstuvwxyz0123456789'


@login_required()
def verify_email(request):
    temp_dict = {}
    return render_to_response(
        'email-verify.html',
        temp_dict, context_instance=RequestContext(request))


@login_required()
def resend_email(request):
    user_profile = request.user.user_profile
    if user_profile and user_profile.is_email_verified == False:
        try:
            email_verify_object = EmailVerification.objects.get(user=request.user, entry_valid=True)
        except:
            email_verify_object = None

        if email_verify_object:
            email_verify_object.entry_valid = False
            email_verify_object.save()
            email_verify_object = EmailVerification()
            email_verify_object.user = request.user
            email_verify_object.email = str(user_profile.user.email)
            email_verify_object.verification_key = get_random_string(20, chars)
            email_verify_object.save()
            subject = "Confirm your email account."
            content = "Please click here <a href='/abcd'></a>"
            try:
                send_mail(subject, content, EMAIL_HOST_USER, [request.user.email], fail_silently=False)
            except:
                pass
            messages.success(request, "Verification mail has been resent.")
        else:
            email_verify_object = EmailVerification()
            email_verify_object.user = request.user
            email_verify_object.email = str(user_profile.user.email)
            email_verify_object.verification_key = get_random_string(20, chars)
            email_verify_object.save()
            subject = "Confirm your email account."
            content = "Please click here <a href='/abcd'></a>"
            try:
                send_mail(subject, content, EMAIL_HOST_USER, [request.user.email], fail_silently=False)
            except:
                pass
            messages.success(request, "Verification mail has been resent.")
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def email_confirmation(request, key=None):
    try:
        email_confirmation_object = EmailVerification.objects.get(verification_key=key, entry_valid=True)
    except:
        email_confirmation_object = None

    if email_confirmation_object:
        try:
            user_profile = email_confirmation_object.user.user_profile
            flag = 1
        except:
            flag = 0

        if flag == 1:
            user_profile.is_email_verified = True
            user_profile.save()
            email_confirmation_object.entry_valid = False
            email_confirmation_object.save()
        messages.success(request, "Email successfully verified.")
    return HttpResponseRedirect('/')

