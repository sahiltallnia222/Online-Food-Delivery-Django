from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from vendor.vendorForm import VendorForm
from .form import UserForm
from django.core.exceptions import PermissionDenied
from .models import User, UserProfile


def check_vendor_role(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

def check_cust_role(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    
    if request.user.is_authenticated :
        messages.warning(request,'You are already logged in.')
        return redirect('accounts:myAccount')
    elif(request.method=='POST'):
        form=UserForm(request.POST)
        if form.is_valid():
            # commit=false means taht assign the values to the user but not save the user
            # in this method create_user method is not working it is directly saving the data
            password=form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.role=User.CUSTOMER
            # user.set_password(password)
            # user.save()
            
            # another way of doing this
            
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            user=User.objects.create_user(first_name,last_name,username,email,password)
            user.role=User.Vendor
            user.save()
            messages.success(request,'Your account has been registered successfully')
            return redirect('accounts:registerUser')

        else:
            print(form.errors)
            messages.error(request,'Something went wrong !')
    
    form=UserForm()
    return render(request,'accounts/registeruser.html',{'form':form})


def registerVendor(request):
    if request.user.is_authenticated :
        messages.warning(request,'You are already logged in.')
        return redirect('accounts:myAccount')
    elif request.method=='POST':
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name,last_name,username,email,password)
            user.role=User.Vendor
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            vendor.user_profile=UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(request,'Your account has been registered for approval')
            return redirect('accounts:registerVendor')
        else:
            print(form.errors)
            print(v_form.errors)
    else:
        v_form=VendorForm()
        form=UserForm()

    context={
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registervendor.html',context)



# messages, we don't need to pass in to the form to access in to any html file because it is passed in to the context_processor which makes it available to all the html files to check open settings templates there is something called context_processor which messages module in written.


def login(request):
    if request.user.is_authenticated :
        messages.warning(request,'You are already logged in.')
        return redirect('accounts:myAccount')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        print(email)
        print(password)
        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in.')
            return redirect('accounts:myAccount')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('accounts:login')
    
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out.')
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='accounts:login')
@user_passes_test(check_cust_role)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')



@login_required(login_url='accounts:login')
@user_passes_test(check_vendor_role)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')