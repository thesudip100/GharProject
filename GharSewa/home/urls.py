from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
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
    path('payment/',views.payment,name='payment')
    ]