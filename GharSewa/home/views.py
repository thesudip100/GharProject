from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string

from home.urls import *
User=get_user_model()

# Create your views here.
def index(request):
    return render(request,'index.html')

# def indexReturn(request):
#      return redirect(index)

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

               stat = Status.objects.get(status='pending')
              
               profRegister.objects.create(firstName=firstName,lastName=lastName,email=email,fullAddress=fullAddress,phone = phone,profilePic = profilePic,experience = experience,training_certificate=training_certificate,user_id=user.id,service=service, city=city,status=stat)
            #    professional_group=Group.objects.get(name='Professional')
            #    professional_group.user_set.add(user)
               return HttpResponse("Professional registered successfully")
     
     context = {'services': services, 'city': city}
     return render(request,'prof_register.html',context)



def handleLogin(request):
     if request.method == 'POST':
          userName=request.POST.get('username')
          passWord=request.POST.get('password')

          user=authenticate(request,username=userName,password=passWord)
          
          if user is not None:
                login(request, user)
                return redirect(index)
                # g=request.user.groups.all()[0].name
                # if g=='Customer':
                #     context=True
                #     return render(request, 'index.html', {'context':context})
                    
                # elif g=='Professional':
                #     context=False
                #     return render(request,'index.html',{'context':context})
          
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
        data = request.POST
        book = Booking.objects.create( professional=prof, customer=client,
                                      book_date=data['date'], book_days=data['day'], book_hours=data['hour'])
        
        # customer_email = request.user.email
        # subject = 'Booking Confirmation from GharSewa'
        # message = "Your booking is confirmed.\n Please view your booking details in the dashboard. \nIf you have any queries, call us or write to us via Contact Us Form. \n\nThank You!"
        # from_email = 'agharsewa@gmail.com'
        # recipient_list = [customer_email]
        # send_mail(subject, message, from_email, recipient_list)

    return render(request, 'booking.html', {'prof': prof, 'customer': client})
    




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


def payment(request):
    return render(request,'payment.html')