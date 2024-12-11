from itertools import product
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib import messages
from django.contrib.auth.models import User,auth
from .form import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate, logout

from .models import *
from . utils import cookieCart, cartData,guestOrder
from .filters import Product_filter
# from .single_prod_selector import get_single_prod

# Create your views here.

# admin

# import csv

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.forms import widgets
# from django.http import HttpResponse
# from django.urls import reverse_lazy
# from django.views.generic import DetailView, ListView, View
# from django.views.generic.edit import CreateView, DeleteView, UpdateView


def store(request):

    data= cartData(request)
    cartItems = data['cartItems']
    
    carousels = Carousel.objects.all()
    products = Product.objects.all()

    user_product_filter = Product_filter(request.GET, queryset=products)

    context={
        'user_product_filter':user_product_filter,
        'carousels':carousels,
        'cartItems':cartItems
    }
    return render(request, 'store/index.html', context)

def cart(request):

    data= cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    data= cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete() 

    return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)


    else:
        customer, order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment complete!', safe=False)


def register(request):
    form = RegisterUserForm()
    if request.method=="POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username','last_name')
            messages.success(request, 'Registered successfully'+user)
            return redirect("login")

    context={
           "form":form
    }
    return render(request, "store/register.html",context) 

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('store')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    
    else:
        return render (request,'store/login.html')   

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")         

# detail view
def single_product(request,productId):

    data= cartData(request)
    cartItems = data['cartItems']
    
    prod = Product.objects.get(pk=productId)
    context={
        "prod":prod,
        'cartItems':cartItems
    }
    return render(request, 'store/single_product.html', context)


# category view

def manage_bags(request):
    data= cartData(request)
    cartItems = data['cartItems']

    bags = Product.objects.filter(status = 'BAGS')
    context={
        'bags':bags,
        'cartItems':cartItems
    }
    return render(request, 'store/bags.html', context)

def manage_men(request):
    data= cartData(request)
    cartItems = data['cartItems']

    men_wear = Product.objects.filter(status = 'MEN')
    context={
        'men_wear':men_wear,
        'cartItems':cartItems
    }
    return render(request, 'store/men_wear.html', context)

def manage_scarves(request):
    data= cartData(request)
    cartItems = data['cartItems']

    scarves = Product.objects.filter(status = 'SCARVES')
    context={
        'scarves':scarves,
        'cartItems':cartItems
    }
    return render(request, 'store/scarves.html', context)

def manage_women(request):
    data= cartData(request)
    cartItems = data['cartItems']

    women_wear = Product.objects.filter(status = 'WOMEN')
    context={
        'women_wear':women_wear,
        'cartItems':cartItems
    }
    return render(request, 'store/women_wear.html', context)

def manage_special_offers(request):
    data= cartData(request)
    cartItems = data['cartItems']

    specials = Product.objects.filter(special_offers = 'YES')
    context={
        'specials':specials,
        'cartItems':cartItems
    }
    return render(request, 'store/special_offers.html', context)

def manage_about_us(request):
    data= cartData(request)
    cartItems = data['cartItems']

    contacts = Contact_us.objects.all()
    context={
        'contacts':contacts,
        'cartItems':cartItems

    }
    return render(request, 'store/about_us.html', context)

def manage_faq(request):
    data= cartData(request)
    cartItems = data['cartItems']
    context={
        'cartItems':cartItems
    }
    return render(request, 'store/faq.html', context)


# how to view

def manage_how_to_order(request):
    data= cartData(request)
    cartItems = data['cartItems']
    context={
         'cartItems':cartItems
    }
    return render(request,'store/how_to_order.html', context)

#  admin view

# class StudentListView(LoginRequiredMixin, ListView):
#     model = Student
#     template_name = "students/student_list.html"


# class StudentDetailView(LoginRequiredMixin, DetailView):
#     model = Student
#     template_name = "students/student_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super(StudentDetailView, self).get_context_data(**kwargs)
#         context["payments"] = Invoice.objects.filter(student=self.object)
#         return context


# class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Student
#     fields = "__all__"
#     success_message = "New student successfully added."

#     def get_form(self):
#         """add date picker in forms"""
#         form = super(StudentCreateView, self).get_form()
#         form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
#         form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
#         form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
#         return form


# class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Student
#     fields = "__all__"
#     success_message = "Record successfully updated."

#     def get_form(self):
#         """add date picker in forms"""
#         form = super(StudentUpdateView, self).get_form()
#         form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
#         form.fields["date_of_admission"].widget = widgets.DateInput(
#             attrs={"type": "date"}
#         )
#         form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
#         form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
#         # form.fields['passport'].widget = widgets.FileInput()
#         return form


# class StudentDeleteView(LoginRequiredMixin, DeleteView):
#     model = Student
#     success_url = reverse_lazy("student-list")


# class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = StudentBulkUpload
#     template_name = "students/students_upload.html"
#     fields = ["csv_file"]
#     success_url = "/student/list"
#     success_message = "Successfully uploaded students"


# class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         response = HttpResponse(content_type="text/csv")
#         response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

#         writer = csv.writer(response)
#         writer.writerow(
#             [
#                 "registration_number",
#                 "surname",
#                 "firstname",
#                 "other_names",
#                 "gender",
#                 "parent_number",
#                 "address",
#                 "current_class",
#             ]
#         )

#         return response
