from django.shortcuts import render,redirect
from django.contrib import messages
from .form import UserForm
# Create your views here.
from .models import User
def registerUser(request):
    
    if(request.method=='POST'):
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
            user.save()
            messages.success(request,'Your account has been registered successfully')
            return redirect('registerUser')

        else:
            print(form.errors)
            messages.error(request,'Something went wrong !')
            return render(request,'accounts/registeruser.html',{'form':form})
    
    form=UserForm()
    return render(request,'accounts/registeruser.html',{'form':form})




# messages, we don't need to pass in to the form to access in to any html file because it is passed in to the context_processor which makes it available to all the html files to check open settings templates there is something called context_processor which messages module in written.