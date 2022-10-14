from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .utils import detectUser,send_verification_email,send_password_reset_email
from django.contrib.auth.decorators import login_required,user_passes_test
from vendor.vendorForm import VendorForm
from .form import UserForm
from django.core.exceptions import PermissionDenied
from .models import User, UserProfile
from django.contrib.auth.tokens import default_token_generator

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
            user.role=User.CUSTOMER
            send_verification_email(request,user)
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
            
            send_verification_email(request,user)
            
            
            messages.success(request,'Your account has been registered for approval')
            return redirect('accounts:registerVendor')
        else:
            # print(form.errors)
            # print(v_form.errors)
            print('error occured')
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


def activate(request,uidb64,token):
    
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulation Your account is activated.')
        return redirect('accounts:myAccount')
    else:
        messages.error(request,'Invalid Activation link')
        return redirect('accounts:myAccount')
    
    
def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            send_password_reset_email(request,user)
            messages.success(request,'Password reset link has been sent to your email account')
            return redirect('accounts:login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('accounts:login')

            
    
    return render(request,'accounts/forgot_password.html')

def reset_password(request):
    
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('accounts:login')
        else:
            messages.error(request,'Password does not match')
    return render(request,'accounts/reset_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request,'This link has been expired.')
        return redirect('accounts:myAccount')