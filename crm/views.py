from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .models import Record

# Create your views here --

def home(request):     
     
    return render(request, 'crm/index.html')

# Register --

def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()             
            return redirect('my-login')
        else:
            pass  
    
    context = {'form': form}
    return render(request, 'crm/register.html', context=context)

# Login --

def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)                
                return redirect('dashboard')   
                
        context = {'form': form}
        return render(request, 'crm/my-login.html', context=context)
    
    # If the request method is not 'POST', return the form
    context = {'form': form}
    return render(request, 'crm/my-login.html', context=context)

# User logout --

def logout(request):
    auth.logout(request)  
    return redirect('my-login')

# Dashboard --

@login_required(login_url='my-login')
def dashboard(request):   
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'crm/dashboard.html', context=context)

# Create a record --

@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm(request.POST)
    
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    else:
        print(form.errors)
    
    context = {'form': form}
    return render(request, 'crm/create-record.html', context=context)

# Update a record --

def update_record(request, pk):
    record = Record.objects.get(id=pk)
    
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UpdateRecordForm(instance=record)
    
    context = {'form': form}
    return render(request, 'crm/update-record.html', context=context)

# Read / View a singular record --

@login_required(login_url='my-login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record': all_records}
    return render(request, 'crm/view-record.html', context=context)

# Delete a record --

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    return redirect('dashboard')