from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):

    def register(self, request):
        errors = []
        first_name_digit = any(char.isdigit() for char in request.POST['first_name'])
        last_name_digit = any(char.isdigit() for char in request.POST['last_name'])
        if len(request.POST['first_name']) <= 2:
            errors.append("First name must be more than 2 characters!")
        if len(request.POST['last_name']) <= 2:
            errors.append("Last name must be more than 2 characters!")
        if first_name_digit == True:
            errors.append("Only alphanumeric characters allowed for the first name field!")
        if last_name_digit == True:
            errors.append("Only alphanumeric characters allowed for the last name field!")
        if len(request.POST['email']) == 0:
            errors.append("Email cannot be blank!")
        elif not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Email not valid!")
        if len(request.POST['password']) < 8:
            errors.append('Password needs to be longer!')
        if request.POST['password'] != request.POST['password_con']:
            errors.append('Passwords must match!')
        if len(errors) is not 0:
            print errors
            return (False, errors)
        elif len(errors) == 0:
            # request.POST['password'] == request.POST['password_con']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = Users.login_mgr.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw_hash=pw_hash)
            print user
            request.session['email'] = request.POST['email']
            # user.save()
            return (True, user)

    def valid_login(self, request):
        from bcrypt import hashpw, gensalt
        errors = []
        if len(request.POST['email_log']) == 0:
            errors.append("Login fields cannot be blank!")
            return (False, errors)
        elif len(request.POST['password_log']) == 0:
            errors.append('Login fields cannot be blank!')
            return (False, errors)
        try:
            if Users.login_mgr.get(email=request.POST['email_log']):
                user = Users.login_mgr.get(email=request.POST['email_log'])
                print user.pw_hash
                password = request.POST['password_log'].encode()
                stored_pw = user.pw_hash.encode()
                if hashpw(password, stored_pw):
                    print hashpw(password, stored_pw)
                    return (True, user)

                else:
                    errors.append("Sorry, that username or password doesn't exist!")
                    print errors
                    return (False, errors)
            else:
                errors.append("Sorry, that username or password doesn't exist!")
                print errors
                return (False, errors)
        except ObjectDoesNotExist:
            errors.append("Sorry, that username or password doesn't exist!")
            return (False, errors)

    def trip_valid(self, request):
        errors = []
        if len(request.POST['destination']) < 1:
            errors.append("Destination cannot be blank!")
        if len(request.POST['description']) < 1:
            errors.append("Description cannot be blank!")
        if request.POST['date_start'] < str(datetime.today()):
            errors.append("Travel date from must be in the future!")
        if request.POST['date_to'] < str(datetime.today()):
            errors.append("Travel date must be in the future!")
        if request.POST['date_to'] < request.POST['date_start']:
            errors.append("The dates must be backwards!")
        if len(errors) is not 0:
            print errors
            return (False, errors)
        elif len(errors) == 0:
            trip = Trips.objects.create(destination=request.POST['destination'], description=request.POST['description'], user_created=request.session['email'], date_start=request.POST['date_start'], date_to=request.POST['date_to'])
            # trip.save()
            print trip
            return (True, errors, trip)

class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    login_mgr = UserManager()
    objects = models.Manager()

class Trips(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_to = models.DateTimeField()
    user_created = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    users = models.ManyToManyField(Users)
    objects = models.Manager()
    trip_mgr = UserManager()
