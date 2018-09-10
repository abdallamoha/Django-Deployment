from django.shortcuts import render
from .form import UserForm, UserProfileInfoForm


#for login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required # if you what a view requid to login


# Create your views here.
def index(request):
    return render(request, 'app/index.html')



@login_required
def special(request):
    return render(request, 'app/special.html')

@login_required
def user_logout(request):
    logout(request) #Remove the authenticated user's ID from the request and flush their session data.
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registerd = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registerd = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app/registration.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registerd': registerd})


def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password) #If the given credentials are valid, return a User object.

        # noinspection PyInterpreter
        if user:
            if user.is_active:
                login(request,user) #login the user.
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('account not active')
        else:
            print ('someone failed login')
            print ('username: {} and password{}'.format(username,password))

            return HttpResponse('invalid login')
    else:
        return render(request,'app/login.html',{})
