# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASS_REGEX = re.compile(r'^\d.*[A-Z]|[A-Z].*\d')



class UserManager(models.Manager):
    def register(self, user_dict):
        error_list = []
        properly_validated = True

        if len(user_dict['first_name']) < 2 or len(user_dict['last_name']) < 2:
            error_list.append('First or Last name too short')
            properly_validated = False

        if len(user_dict['password']) < 8:
            error_list.append('Password is too short')
            properly_validated = False

        if user_dict['password'] != user_dict['confirm_password']:
            error_list.append('Passwords do not match')
            properly_validated = False

        if not EMAIL_REGEX.match(user_dict['email']):
            error_list.append('First or Last name too short')
            properly_validated = False
            
        if not NAME_REGEX.match(user_dict['first_name']):
            error_list.append('Name can only have letters')
            properly_validated = False

        if not NAME_REGEX.match(user_dict['last_name']):
            error_list.append('Name can only have letters')
            properly_validated = False

        # if not PASS_REGEX.match(user_dict['password']):
        #     error_list.append('Password requires upper case and special character')
        #     properly_validated = False
        
        if properly_validated == True:
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(str(user_dict['password']), salt)
            try:
                User.objects.create(first_name=user_dict['first_name'], last_name=user_dict['last_name'], email=user_dict['email'], password=hashed_pw, salt=salt)
                return (properly_validated)
            except:
                properly_validated = False
                error_list.append('Email is already registered')
                return(properly_validated, error_list)
        else:
            return(properly_validated, error_list)
    
    
    
    
    def login(request, user_dict):
        error_list = []
        properly_logged = True
        try:
            user = User.objects.get(email=user_dict['email'])
        except:
            properly_logged = False
            error_list.append("Email does not exist, please register")
            return(properly_logged, error_list)
        
        if bcrypt.hashpw(str(user_dict['password']), str(user.salt)) != user.password:
            properly_logged = False
            error_list.append("Password invalid")
            return (properly_logged, error_list)

        else:
            return (properly_logged, error_list) 













class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100, default="$2b$12$pTnZS9g9dWx1ZveqSkHL5e")
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    
class Review(models.Model):
    review = models.CharField(max_length=100)
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name="reviews")
    created_at= models.DateTimeField(auto_now_add=True) 
    updated_at= models.DateTimeField(auto_now=True) 
    
