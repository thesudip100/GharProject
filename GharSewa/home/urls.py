from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.aboutPage, name='about'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('prof_register/', views.prof_register, name='prof_register'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('contact/',views.contact, name='contact'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('services/', views.services, name='services'),
    path('services/<int:myid>/', views.serviceView, name='serviceView'),
    path('booking/<int:pid>', views.customerBooking, name='booking'),
    path('verify/', views.verify, name='verify'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('bookingdetails/',views.booking_detail,name='bookingdetails'),
    path('user_booking/', views.profBooking, name='user_booking'),
    path('cancel/<int:cancel_id>/', views.cancelBooking, name='cancelBooking'),
    ]