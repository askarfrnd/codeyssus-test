codeyssus-test
==============

This is a demo django project for user registration and login. 
Login involves normal login as well as social login. (facebook and twitter)

Ensures uniquity of email ID's.

Dependencies:
-------------
python 2.7

django 1.7

django-allauth 0.18.0

Inorder to make it work:
------------------------
1. Create local_settings.py file with database connectivity details.
2. Fill in the site details at adminpanel and ensure it is callable with settings.SITE_ID(django.contrib.sites app).
3. Add Social App(socialaccount app) for each OAuth based provider in adminpanel. (Mandatory Fields: Client ID, Secret Key, Sites)

