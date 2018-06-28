from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse


def index(request):
    context = {
        'users' : User.objects.all()}
    return render(request, 'beltexam_app/index.html', context)

def process(request):

    action = request.POST['action']

    if action == "register":

        result = User.objects.regValidator(request.POST)

        if result[0]:
            request.session['id'] = result[1].id
            request.session['fullname'] = result[1].fullname
            return redirect("/dashboard")
        else:
            error_list = result[1]
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
    if action == "login":
        result = User.objects.loginValidator(request.POST)
        print("receiving result")
        print(result)

        if result[0]:
            request.session['id'] = result[1].id
            request.session['fullname'] = result[1].fullname
            return redirect("/dashboard")
        else:
            error_list = result[1]
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')

    if action == "addproduct":
        result = Product.objects.productValidator(request.POST, request.session['id'])
        print("receiving result")
        print(result)
        if result[0]:
            return redirect("/dashboard")
        else:
            error_list = result[1]
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/add')

def dashboard(request):


    if 'id' not in request.session:
        return redirect("/")
    else:

        context = {

            'mywish' : Product.objects.filter(person_id = request.session['id'])|Product.objects.filter(wishes__wanter_id= request.session['id']),
            'otherwish' : Product.objects.exclude(person_id = request.session['id']) & Product.objects.exclude(wishes__wanter_id= request.session['id'])
        }

    return render(request, "beltexam_app/dashboard.html", context)

def wish_items(request, product_id):
    if 'id' not in request.session:
        return redirect("/")

    context = {
        'wishinfo' : Product.objects.get(id = product_id),
        'wishpeople' : Product.objects.get(id = product_id).wishes.all()
    }

    return render (request, "beltexam_app/wish_items.html", context)


def wish(request, wishitem_id):
    
    if 'id' not in request.session:
        return redirect("/")
    elif Wish.objects.filter(wanter_id = request.session['id'], wishitem_id = wishitem_id):
        return redirect("/dashboard")
    else:
        Wish.objects.create(wanter_id = request.session['id'], wishitem_id = wishitem_id)
    
    return redirect("/dashboard")

def remove(request, id):
    
    Product.objects.get(id = id).delete()

    return redirect('/dashboard')


def removewish(request, wanter_id):
    
    Wish.objects.get(wanter_id = request.session['id']).delete()
    return redirect('/dashboard')


def add(request):

    return render(request, "beltexam_app/add.html")
    

def logout(request):
    request.session.clear()
    return redirect("/")


