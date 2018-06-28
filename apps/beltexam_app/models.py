from django.db import models
import re
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []

        fullname = form['fullname']
        username = form['username'].lower()
        password = form['password']
        confirm_pw = form['confirm_pw']
        start = form['start']


        if not fullname:
            errors.append("Your name is required.")
        elif len(fullname) < 3:
            errors.append("Your name must be at least 3 characters.")
        elif not fullname.isalpha():
            errors.append("Your name cannot contain numbers.")
        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Your username must be at least 3 characters.")
        else:
            users = User.objects.filter(username = username)
            if users:
                errors.append("Username already exists. Please login.")
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Your password must be at least 8 characters.")
        if not confirm_pw:
            errors.append("Confirm password is required.")
        if password != confirm_pw:
            errors.append("Passwords must match.")
        if not start:
            errors.append("Date/Time for Hired Date is required.")
        elif start > str(datetime.now()):
            errors.append("Hired date cannot be a future date!")

        if not errors:
            # save user in database
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(fullname=fullname, username=username, password=hash_pw, start=start)
            return (True, user)
        else:
            return (False, errors)


    def loginValidator(self, form):
        errors = []

        username = form['username'].lower()
        password = form['password']

        if not username:
            errors.append("username is required.")
        else:
            users = User.objects.filter(username = username)
            if not users:
                errors.append("Username not in database. Please register.")
            else:
                user = users[0]
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors.append("Password does not match password in database.")
        if not password:
            errors.append("Password is required.")

        if not errors:
            user = User.objects.get(username = username)
            return (True, user)
        else:
            return (False, errors)


class ProductManager(models.Manager):

    def productValidator(self, form, id):

        errors = []

        item = form['item']

        if not item:
            errors.append("Item name is required.")
        elif len(item) < 3:
            errors.append("Item name must be at least 3 characters.")
        if not errors:
            # save user in database
            product = Product.objects.create(item=item, person_id=id)
            # trip = Trip.objects.create(traveler_id = id, trip_id = travel.id)
            return (True, Product)
        else:
            return (False, errors)


class User(models.Model):
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=15)
    start = models.DateTimeField('%Y-%m-%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User: {} {}>".format(self.fullname, self.username)

class Product(models.Model):
    item = models.CharField(max_length=255)
    person = models.ForeignKey(User, related_name="adder")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __repr__(self):
        return "<Product: {}>".format(self.item)

class Wish(models.Model):
    wishitem = models.ForeignKey(Product, related_name="wishes")
    wanter = models.ForeignKey(User, related_name="wisher")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<Wish: {}>".format(self.wishitem)