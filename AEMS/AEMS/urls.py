"""
URL configuration for AEMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('user',views.user,name='user'),
    path('manager',views.manager,name='manager'),
    path('admins',views.admins,name='admins'),
    path('logout',views.signout,name='logout/'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('msignup',views.msignup,name='msignup'),
    path('signout',views.signout,name='signout'),
    path('contact',views.contact,name='contact'),
    path('check_status/', views.check_status, name='check_status'),
    path('book_equipment',views.book_equipment,name='book_equipment'),
    path('book-equipment/', views.book_equipment, name='book_equipment'),
    path('update-booking-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]
