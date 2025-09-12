# File: quotes/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file contains the views/functions for the quotes app.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random 

# Global list of Quotes and Images 

QUOTES = [
    "Is mayonnaise an instrument?",
    "Knowledge can never replace friendship. I prefer to be an idiot.",
    "The inner machinations of my mind are an enigma." , 
]

IMAGES = [
    "https://people.com/thmb/e7fznawoCByHxbQhKe6gZlL5IMo=/4000x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(1179x518:1181x520)/patrick-star-8e4a58d3c48848f2ad27fec739062890.jpg",
    "https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUydm55aGljZnZwZTl0bWYyMjJrcW9nNm9tandvN2Z4bDFxbXFuNTF6aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26FLdmIp6wJr91JAI/giphy.gif",
    "https://assets.nick.com/uri/mgid:arc:imageassetref:ws.kids.com:bd09be5c-2d6a-4b82-ba32-fd8aabac45ec?quality=0.7&gen=ntrn&format=webp&crop=true&width=660",
]


# Create your views here.

def quote_page(request):
    '''Respond to the URL 'quotes' and returns a rendered template with a 
    random quote and image.'''

    template_name = "quotes/quote.html"

    context = {
        "time": time.ctime(),
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }

    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL 'show_all' and returns a rendered template with
    all quotes and images.'''

    template_name = "quotes/show_all.html"

    context = {
        "time": time.ctime(),
        "all_quotes": QUOTES,
        "all_images": IMAGES,
    }

    return render(request, template_name, context)

def about(request): 
    '''Respond to the URL 'about' and returns a rendered template with 
    basic information about the app.'''

    template_name = "quotes/about.html"

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)