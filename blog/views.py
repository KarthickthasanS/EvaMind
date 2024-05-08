from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from blog.models import Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import random
import re

def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs, 'current_page': 'blog'}
    return render(request, 'blog.html', context)



def blogpost (request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
        context = {'blog': blog, 'current_page': 'blogpost'}
        return render(request, 'blogpost.html', context)
    except Blog.DoesNotExist:
        context = {'message': 'Blog post not found'}
        return render(request, '404.html', context, status=404)


def blogsearch(request):
    query = request.GET.get('q')
    query_list = query.split()
    results = Blog.objects.none()
    for word in query_list:
        results = results | Blog.objects.filter(Q(title__contains=word) | Q(content__contains=word)).order_by('-time')
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    if len(results) == 0:
        message = "Sorry, no results found for your search query."
    else:
        message = ""
    return render(request, 'blogsearch.html', {'results': results, 'query': query, 'message': message})     


def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by('-time')
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "category.html", {"message": message})
    paginator = Paginator(category_posts, 3)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    return render(request, "category.html", {"category": category, 'category_posts': category_posts})
    

    