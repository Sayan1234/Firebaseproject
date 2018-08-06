from django.conf import settings
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.core.mail import send_mail

config = {
    "apiKey": "AIzaSyAFAlUlIebQuUUCMbMW2VQoBeiShtmwsHw",
    "authDomain": "backendassignment-120f0.firebaseapp.com",
    "databaseURL": "https://backendassignment-120f0.firebaseio.com",
    "projectId": "backendassignment-120f0",
    "storageBucket": "backendassignment-120f0.appspot.com",
    "messagingSenderId": "993847355059"
  }

firebase=pyrebase.initialize_app(config)
db=firebase.database()

authe=firebase.auth()

def signIn(request):
      return render(request,"signIn.html")

def postsign(request):
    username=request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message="Invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    print("info "+str(a))
    data={
        "username":username,
        "email":email
    }
    back=""
    confirm=""
    olduser=db.child('users').child(a).child('email').get().val()
    db.child('users').child(a).set(data)
    db.child('userinformation').child(a).set(data)
    
    # print(olduser)
    if olduser==None:
        send_mail(
        'Hello',
        'Dear '+username+", Welcome to our app",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )
        confirm="Email sent successfully"

    else:
        back="back"
    
    # users=db.child("users").child(a).get()
    # print(users.val())
    return render(request,"welcome.html",{"e":back+" "+username+" "+confirm})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')