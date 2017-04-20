# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, "book_reviews/index.html")


def home_page(request):
    context = {
        'books': Book.objects.all(),
        'reviews': Review.objects.all().order_by("-created_at")[:3],
        'user': User.objects.all()
    }
    
    return render(request,'book_reviews/home.html', context)


def book_page(request,id):
    context = {
        'book' : Book.objects.get(id=id),
        'reviews': Review.objects.filter(book_id=id).order_by('-created_at'),
        'user': User.objects.all() 
    }

    return render(request, 'book_reviews/book.html', context)





def add_book(request):
    context={
        'unique_authors': Book.objects.values('author').distinct()
    }



    return render(request, "book_reviews/add_book.html", context)

def register(request):
    print 'register works'
    if request.method == 'POST':
        user_dict = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password']            
            }
        register_result = User.objects.register(user_dict)

        if register_result == True:
            request.session['first_name'] = request.POST['first_name']
            request.session['email']  = request.POST['email'] 
            return redirect('book_reviews:homepage')
        
        elif register_result[0] == False:
            for message in register_result[1]:
                messages.add_message(request, messages.ERROR, message)
        
    return redirect('book_reviews:index')

def logout(request):
    for key in request.session.keys():
        del request.session[key]

    return redirect('book_reviews:index')
    

def login(request):
    if request.method == 'POST':
        user_dict = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        login_result = User.objects.login(user_dict)
        

        if login_result[0] == True:
            user = User.objects.get(email=user_dict['email'])
            request.session['email']=user.email
            request.session['first_name'] = user.first_name
            print request.session['first_name']
            return redirect('book_reviews:homepage')
        if login_result[0] == False:
            for message in login_result[1]:
                messages.add_message(request, messages.ERROR, message)
            
    return redirect('book_reviews:index')

def create_book(request):
    if request.method == "POST":
        book = None
        try:
            book = Book.objects.get(title=request.POST['title'])
            #redirect to route with book and reviews
        except:
            book = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
            
        rating = request.POST['stars']
        user= User.objects.get(email=request.session['email'])

        review = Review.objects.create(review=request.POST['review'], rating=int(rating), book=book, user = user)

    return redirect('book_reviews:homepage')

def create_review(request, id):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        book = Book.objects.get(id=id)
        print type(book)
        rating = int(request.POST['stars'])
        Review.objects.create(review=request.POST['review'], rating=rating, book=book,user=user)

    return redirect(reverse('book_reviews:book_page', kwargs={'id': id}))


def user_page(request, id):
    context = {
        'user': User.objects.filter(id=id).annotate(num_reviews=Count('reviews'))[0],
    }
    return render(request, "book_reviews/user.html",context)

def delete_review(request, id, book_id):

    instance = Review.objects.get(id=id)
    instance.delete()
    return redirect(reverse('book_reviews:book_page', kwargs={'id':book_id}))





