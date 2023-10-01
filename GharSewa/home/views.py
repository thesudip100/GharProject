from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests
import json

from home.urls import *


# Create your views here.
def index(request):
    print("You are :", request.session.get('username'))
    print("You are :", request.session.get('user_id'))
    return render(request,'index.html')

def aboutPage(request):
    return render(request,'about.html')


def customer_register(request):
        user="none"
        if request.method=='POST':
             username=request.POST['customer_username']
             firstName=request.POST['customer_fname']
             lastName=request.POST['customer_lname']
             email=request.POST['customer_email']
             phone=request.POST['customer_phone']
             fullAddress=request.POST['customer_address']
             password1=request.POST['customer_pass1']
             password2=request.POST['customer_pass2']
             profilePic=request.FILES['customer_image']

             if password1==password2:
                user=User.objects.create_user(first_name=firstName,last_name=lastName,password=password1,username=username,email=email)
                user.save()
                userRegister.objects.create(firstName=firstName, lastName=lastName, email=email, phone=phone, fullAddress=fullAddress,user_id=user.id,profilePic=profilePic)
                # customer_group=Group.objects.get(name='Customer')
                # customer_group.user_set.add(user)  
                return HttpResponse("Successfully registered customer")
        
        return render(request,'user_register.html')

                      

def prof_register(request):

     user = "none"
     services = Service.objects.all()
     city = City.objects.all()
     if request.method == "POST":

          userName = request.POST['user_username']
          firstName = request.POST['user_fname']
          lastName = request.POST['user_lname']
          email = request.POST['user_email']
          phone = request.POST['user_phone']
          fullAddress = request.POST['user_address']
          password1 = request.POST['user_pass1']
          password2 = request.POST['user_pass2']
          profilePic = request.FILES['image']
          experience = request.POST['exp']
          training_certificate = request.FILES['cert']

          
          if password1==password2:
               user = User.objects.create_user(first_name=firstName,last_name=lastName,password = password1,username=userName,email=email)
               user.save()

               service = Service.objects.get(service_id=request.POST['service'])
               city = City.objects.get(id=request.POST['city'])

              
               profRegister.objects.create(firstName=firstName,lastName=lastName,email=email,fullAddress=fullAddress,phone = phone,profilePic = profilePic,experience = experience,training_certificate=training_certificate,user_id=user.id,service=service, city=city,)

               return HttpResponse("Professional registered successfully")
     
     context = {'services': services, 'city': city}
     return render(request,'prof_register.html',context)



def handleLogin(request):
     if request.method == 'POST':
          userName=request.POST.get('username')
          passWord=request.POST.get('password')

          user=authenticate(request,username=userName,password=passWord)
          
          if user is not None:
                request.session['username']=user.username
                request.session['user_id']=user.id
                login(request, user)
                return redirect(index)
          
     return render(request, 'login.html')

def admin_login(request):
#     if request.user.is_authenticated:
#         messages.info(request, 'You are already logged in!!')
#         return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('logusername')
        password = request.POST.get('logpass')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

    return render(request, 'admin_login.html')

def handleLogout(request):
    logout(request)
    return redirect('/.')

@login_required(login_url='login')
def edit_profile(request):
    u = User.objects.get(id=request.user.id)
    

    try:
        page = True
        user = profRegister.objects.get(user=u)
  
        

    except:
        page = False
        user = userRegister.objects.get(user=u)
        

    services = Service.objects.all()
    city = City.objects.all()

    if request.method == 'POST':
        data = request.POST

        try:
            image = request.FILES['image']
            user.profilePic = image
            user.save()
        except:
            pass

        try:
            user.experience = data['exp']
            serv = Service.objects.get(service_id=data['service'])
            ct = City.objects.get(id=data['city'])
            user.service = serv
            user.city = ct
            certificate = request.FILES['cert']
            user.training_certificate = certificate
            user.save() 
            
        except:
            pass
        
        user.fullAddress = data['address']
        user.phone = data['phone']
        u.username = data['username']
        user.firstName = data['fname']
        user.lastName = data['lname']
        user.email = data['email']
        u.first_name=data['fname']
        u.last_name=data['lname']
        u.email = data['email']

        u.save()
        user.save()
        messages.success(request, 'Profile Updated!!')
        return redirect('profile')

    context = {'page': page, 'services': services, 'city': city, 'user': user}
    return render(request,'editprofile.html',context)


@login_required(login_url='login')
def profile(request):
    users = User.objects.get(id=request.user.id)

    try:
        page = False
        profile = userRegister.objects.get(user=users)

    except:
         page=True
         profile=profRegister.objects.get(user=users)

    return render(request, 'profile.html',{'profile': profile,'page': page})



# Customer Booking
@login_required(login_url='login')
def customerBooking(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        client = userRegister.objects.get(user=request.user)  
    except:
        messages.error(request, 'You must be customer to book a service!!')
        return redirect('services')

    prof = profRegister.objects.get(user=pid)
    
 

    # book=Booking.objects.get(customer=client)

    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        return_url = request.POST.get("return_url")
        amount = request.POST.get("amount")
        purchase_order_id = request.POST.get("purchase_order_id")

        print("return_url::::::",return_url)


        payload = json.dumps({
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
            "name": request.user.username,
            "email": request.user.email,
            "phone": "9800000001"
            }
        })
        headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        new_response = json.loads(response.text)
        data = request.POST
        book = Booking.objects.create( professional=prof, customer=client,
                                                book_date=data['date'], book_days=data['day'], book_hours=data['hour'])
        
        return redirect(new_response['payment_url'])
    
        

        

    return render(request, 'booking.html', {'prof': prof, 'customer': client})
            

def verify(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get('pidx')
    headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json',
        }
    payload = json.dumps({
        'pidx': pidx
    })
    response = requests.request("POST", url, headers=headers, data=payload)  
    print(response.text)
    new_response = json.loads(response.text)

    if new_response['status'] =="Completed":  
        customer_email = request.user.email
        subject = 'Booking Confirmation from GharSewa'
        message = "Your booking is confirmed.\n Please view your booking details in the dashboard. \nIf you have any queries, call us or write to us via Contact Us Form. \n\nThank You!"
        from_email = 'agharsewa@gmail.com'
        recipient_list = [customer_email]
        print("customer_email: ", customer_email)
        print("recipient_list: ", recipient_list)
        send_mail(subject, message, from_email, recipient_list)


    return redirect('/.')
    


def contact(request):
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if name != "" and email != "" and phone != "" and content != "":
            mycontact = Contact(name=name, email=email,
                                phone=phone, content=content)
            mycontact.save()
            messages.success(
                request, 'Thank You For submitting form. We will reach you ASAP!!')

        else:
            messages.error(request, 'Please Fill Up the Form Correctly!!')

    return render(request, 'contact.html')


def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def serviceView(request, myid):
    service = Service.objects.filter(service_id=myid)[0]
    professionals = profRegister.objects.filter(service=service) 

    context = {'service': service, 'professionals': professionals}

    return render(request, 'service_view.html', context)



@login_required(login_url='login')
def booking_detail(request):
    page = True
    user = User.objects.get(id=request.user.id)
    try:
        customer = userRegister.objects.get(user=user)
        books = Booking.objects.filter(customer=customer).order_by('-book_date')
    except:
        return redirect('user_booking')

    context = {'books': books, 'page': page}
    return render(request, 'bookingdetails.html', context)

@login_required(login_url='login')
def profBooking(request):
    page = False
    user = User.objects.get(id=request.user.id)

    serv = profRegister.objects.get(user=user)
    books = Booking.objects.filter(professional=serv)

    context = {'books': books, 'page': page}
    return render(request, 'bookingdetails.html', context)

@login_required(login_url='login')
def cancelBooking(request,cancel_id):
    ser = Booking.objects.get(id=cancel_id)
    ser.delete()
    return redirect('bookingdetails')