# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

#import pakege of register,login and authentication 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here.
from  .models import *
from .signals import *
#////////

#import class of forms

from .forms import orderForm, CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only


#create and view register page
@unauthenticated_user
def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			#messages.success(request, 'Account was created for ' + user)

			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context,)


#create and view login page
@unauthenticated_user

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username of Password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context,)


#create the logout page
def logOut(request):
	logout(request)
	return redirect('login')


#User Profile page 
@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Deliveryed').count()
	pending = orders.filter(status='Pendign').count()

	context = {'orders':orders,
	'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/user.html', context,)


#account setting function 
@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_setting.html', context,)




#dashboard page request and views 
@login_required(login_url='login')
@admin_only
def home(request):

	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Deliveryed').count()
	pending = orders.filter(status='Pendign').count()

	context = {'orders':orders, 'customers':customers, 'total_customers':total_customers,
	'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/dashboard.html', context,)

#product page request and views 
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):

	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

#Customer page request and view 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	order_count = orders.count()
	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'accounts/customer.html', context)


#Create order page and request the view
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
	form = orderForm()
	
	if request.method == 'POST':
		#print('Printng POST:', request.POST)
		form = orderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

#update orders 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = orderForm(instance=order)

	if request.method == 'POST':
		#print('Printng POST:', request.POST)
		form = orderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)
	
#Delete orders
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)






