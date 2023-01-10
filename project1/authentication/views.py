from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from auth import settings
from django.core.mail import send_mail
import pandas as pd
import matplotlib.pyplot as plt
import os
import statistics
from scipy.stats import kurtosis
import math
from .models import *
import cv2,threading
from django.http import StreamingHttpResponse
# Create your views here.

def rmsValue(arr, n):
    square = 0
    mean = 0.0
    root = 0.0
     
    #Calculate square
    for i in range(0,n):
        square += (arr[i]**2)
     
    #Calculate Mean
    mean = (square / (float)(n))
     
    #Calculate Root
    root = math.sqrt(mean)
     
    return root
# Graph plot section
    # plt.style.use('bmh')
    # plt.plot(csv["value"])

# def graph(request):
#     # Create the graph using Matplotlib
#     file="./static/data/HL29.csv"
#     csv=pd.read_csv(file)
#     plt.plot(csv)
#     plt.ylabel('value')

#     # Save the figure to a file
#     plt.savefig('static/graph.png')

    # Construct the HTML string for the image tag
    # html = f"<img src='{{% static 'graph.png' %}}'>"
    # print(html)
    # Return an HttpResponse with the HTML string as the content
    # return HttpResponse(html)


def home(request):
    # print(os.getcwd())
    file="./static/data/HL29.csv"
    csv=pd.read_csv(file)
    arr=csv["value"]
    mean=round(sum(arr)/len(arr),10)
    mini=round(min(arr),10)
    std=round(statistics.stdev(arr),10)
    skw=round(arr.skew(axis=0,skipna=True),10)
    maxi=round(max(arr),10)
    rms=round(rmsValue(arr,len(arr)),10)
    kt=round(kurtosis(arr, fisher=False),10)

    # Turn off interactive mode
    # plt.ioff()

    # plt.ylabel('value') 
    # plt.plot(csv)
    # #Save the figure to a file
    # plt.savefig('static/graph.png')

    # Construct the HTML string for the image tag
    #html = f"<img src='{{% static 'graph.png' %}}'>"
    #print(html)
    

    # Getting Machine Result Value From DataBase
    #x=Score.objects.latest('datetime')
    machineOnOffStatus = Score.objects.order_by('-pk').first().result
    machineOnOffStatusText=""
    btnText=""
    color=""
    if(machineOnOffStatus ==1 ):
        machineOnOffStatusText="ON"
        btnText="Turn OFF"
        color="#04AA6D"
    else : 
        machineOnOffStatusText="OFF" 
        btnText="Turn ON" 
        color="black"
    
    return render(request,"authentication/index.html",{"mean":mean,"min":mini,"std":std,"skw":skw,
    "max":maxi,"rms":rms,"Kutosis":kt,"val":settings.CB,"mos":machineOnOffStatusText,"bt":btnText,"color":color})

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
        message = "Hello "+ myuser.name +"!! \n Welcome to iot Major Project \n You can now Access the IOT Major Project Website with the credintials you entered on sign up Time ! \n Have a Good Day !"
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


from datetime import datetime

def current_time(request):
    now = datetime.now()
    html = f"<html><body>It is now {now}.</body></html>"
    return HttpResponse(html)   