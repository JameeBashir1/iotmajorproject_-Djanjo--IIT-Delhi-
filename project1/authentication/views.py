from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from auth import settings
from django.core.mail import send_mail
from email.message import EmailMessage
from django.utils.http import urlsafe_base64_decode
# Create your views here.
def home(request):
    return render(request,"authentication/index.html")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        specialKey=request.POST['specialKey']
        if (specialKey!=settings.SPECIAL_KEY):
            messages.error(request,"Invalid Special Key")
            return redirect('home')
        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please Try another")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered!")
            return redirect('home')
        if len(username)>20:
            messages.error(request,"Username must be under 20 characters")
            return redirect('home')  
        if not username.isalnum():
            messages.error(request,"User must be Alpha Numeric")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Passwords didn't match!")
            return redirect('home')
    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.name=name
        myuser.save()

        #Email Welcome

        subject = "welcome to iot major project!"
        message = "Hello "+ myuser.name +"!! \n Please confirm email address"
        from_email =settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect('signin')
    return render(request,"authentication/signup.html")    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            uname=user.username
            return render(request,"authentication/index.html",{'name':uname})
        else:
            messages.error(request,"Bad Crediantials") 
            return redirect('home')   
    return render(request,"authentication/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('home')         

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active=True   
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html ')    