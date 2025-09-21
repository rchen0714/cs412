# File: restaurant/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the restaurant app.

from django.shortcuts import render

# Create your views here.


import time
import random 

# All images and dictionaries used for the restaurant app 


IMAGES = [
    "https://lh3.googleusercontent.com/gps-cs-s/AC9h4np-XzekJycx4UrmdYYIRW2NScZQGy7qnUbUJxtR9R2Dk9GcJCcV2XqwJqEOjiKwRQ8hUX4WtBLdVs4bODjZfd7PHhqL5s3aKqcua1ezEEmV2VlPPoBAlaJ1vq0nsK6_EIBngYJk=s1360-w1360-h1020",
    "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nrWWiIp0wj2tBcfM8lIplWxZtqj67WjzgmpcHB4WHmnKsRL5_-yxejRyCHeaYG7JHuhjceMqPtdulD0EfKWLIT7xUKK7f3xq58r4eQvaJcBltSrYGQb-47YZ9HSxubsqZQqpbT4BPartMfw=s1360-w1360-h1020",
    "https://lh3.googleusercontent.com/proxy/NQSWU7fkhgsY24dNMpkzheIutcLH_-phUsQln013rx7oRkvtLr65XHtMWjPAzzHzMfDfTIKTAj0lbDhzzZGqfpigxpu4C9ss94H9_lWHN0wDF6C_edJVWWEsVixttNU6dpwAXoWugwutXQ7CWTj7bHlNOZ4zXQ=s1360-w1360-h1020",
    "https://lh3.googleusercontent.com/proxy/cUnBxxeDE0tb4fBvYtJAbCni0EqoRXJIwo3moEKUCrR0_BemHcbVFr2xHe1hrrOB4ekTReKPhzArWE5wX0QF0Tuuw9V83hoHX--2xGJubcEfaG8XCwbOImuXb3ioMBPKDiqVXw_snzE1arCgcR_I5lIUK2uXhag=s1360-w1360-h1020"
]

main_image = "https://lh3.googleusercontent.com/gps-cs-s/AC9h4npVmalxD7EXSLl4MddXibZj8Z880Q4FHBIKcxY2j1FWkMXWGMGcM1WL_CTWImOPmRFaCnZnSiAnl_leUzcIruBwjKyVqXxS-CFC9PKU3gvw427dsyW_8SyKb42IBKmWNB-8vDE=s1360-w1360-h1020"
location_image = "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqITpksYjqRscVOlV6Ggjp4d5vGNVpnmVrXKlLu1zB42V7ICbR66oxyd6Dk5S0D-Xg8BFBl_mmmvQ2uNJ56jtJeBq3aVn-v0PFtncAfhIb1Ock439pncrgoI2beauXK4Dxu4cF3=s1360-w1360-h1020"

daily_specials = [
    ('Lychee Pandan Toast', 8),
    ('Mango Sticky Rice Pudding', 6.5),
    ('Ube Cheesecake', 6.5),
    ('Thai Iced Bingsoo', 8.75),
]

menu_items = [
    ('Strawberry Snow Bingsoo', 11.95),
    ('Mango Sticky Rice bingsoo', 11.95),
    ('Thai Tea Bingsoo', 11.95),
    ('Nutella French Toast', 12),
    ('Thai Tea Custard Toast', 13),
    ('Banana and Nutella Croffle', 7.95),
    ('Floss pork & Chili paste Croffle', 8),
    ('Ice Cream Croffle', 6.5),
]


def main(request):
    '''Respond to the URL 'restaurant/main' and returns a rendered
    main page'''

    template_name = "restaurant/main.html"

    context = {
        "time": time.ctime(),
        "all_images": IMAGES,
        "main_image": main_image,
        "location_image": location_image,
    }

    return render(request, template_name, context)


def order(request):
    '''Respond to the URL 'restaurant/order' and returns a rendered
    order page'''

    template_name = "restaurant/order.html"
    random_daily = random.choice(daily_specials)

    all_menu = [random_daily] + menu_items

    context = {
        "time": time.ctime(),
        "random_daily": random_daily,
        "all_menu": all_menu,
    }

    return render(request, template_name, context)

def confirmation(request):
    ''' Process the form submission '''

    template_name = "restaurant/confirmation.html"

    if request.POST:

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        instructions = request.POST['instructions']

        cust_cart = request.POST.getlist('cart_items')
        final_cart, total = return_total(cust_cart)

        context = {
            "time": time.ctime(),
            "random_time": random.randint(30, 60),
            "name": name,
            "email": email,
            "phone": phone,
            "final_cart": final_cart,
            "total": total,
            "instructions": instructions,
        }

    return render(request, template_name=template_name, context=context)

def return_total(selected_items):
    ''' Given a list of selected items, return the total price '''

    total = 0
    final_cart=[]
    
    all_items = dict(daily_specials + menu_items)
    
    for item in selected_items:
        if item in all_items:
            total += all_items[item]
            final_cart.append((item, all_items[item]))

    return final_cart, total