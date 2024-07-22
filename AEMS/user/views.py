from django.template.loader import get_template
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from .models import users,HelpRequest
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import JsonResponse


def is_admin(user):
    return user.is_superuser
def is_user(user):
    return user.groups.filter(name='user').exists()
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = { "form": form }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username,password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('dashboard')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)



def signout(request):
    logout(request)
    #using django.contribs logouts the user
    return redirect('login')


def signup(request):
    if request.method == "GET":

        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)

        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user.id,user.username)
            user_data = users(username=user.username,password=user.password)
            user_data.save()
            my_doctor_group = Group.objects.get_or_create(name='user')
            my_doctor_group[0].user_set.add(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admins')
    elif is_user(request.user):
        return redirect('user')
    else:
        return redirect('manager')

@login_required(login_url='login')
@user_passes_test(is_admin)
def msignup(request):
    if request.method == "GET":

        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'msignup.html', context=context)
    else:
        form = UserCreationForm(request.POST)

        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user.id,user.username)
            user_data = users(username=user.username,password=user.password)
            user_data.save()
            my_doctor_group = Group.objects.get_or_create(name='Manager')
            my_doctor_group[0].user_set.add(user)
            if user is not None:
                return redirect('admins')
        else:
            return render(request, 'msignup.html', context=context)



def index(request):
    eqp=Equipment.objects.all()
    return render(request, 'index.html',{'eqp':eqp})


from django.shortcuts import render
from .models import HelpRequest

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        help_text = request.POST.get('help_text')
        help_request = HelpRequest(username=name, email=email, help_text=help_text)
        help_request.save()
        return render(request, 'index.html')

    return render(request, 'contact.html')



from django.shortcuts import render
from .models import Equipment, Booking

def user(request):
    eqp=Equipment.objects.all()
    return render(request, 'user.html', {'eqp': eqp})

from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Equipment, Booking

from django.shortcuts import render, redirect
from .models import Equipment, Booking

@login_required(login_url='login')
def book_equipment(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        equipment_id = request.POST['equipment']
        land = request.POST['land']
        date = request.POST['date']
        
        equipment = Equipment.objects.get(id=equipment_id)
        
        booking = Booking(
            name=name,
            phone_number=phone_number,
            address=address,
            equipment=equipment,
            land=land,
            date=date,
            status='pending'
        )
        booking.save()
        return redirect('user')
    
    equipments = Equipment.objects.all()
    return render(request, 'user.html', {'equipments': equipments})



@login_required(login_url='login')
def update_booking_status(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    new_status = request.POST.get('status')

    if new_status != booking.status:
        if booking.status == 'confirmed' and new_status != 'confirmed':
            booking.equipment.number += 1
        elif booking.status != 'confirmed' and new_status == 'confirmed':
            booking.equipment.number -= 1

        booking.equipment.save()
        booking.status = new_status
        booking.save()

    return redirect('user')

@login_required(login_url='login')
@receiver(post_save, sender=Booking)
def update_equipment_availability(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        instance.equipment.number -= 1
    elif instance.status != 'confirmed':
        instance.equipment.number += 1
    instance.equipment.save()


@login_required(login_url='login')
def check_status(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        
        bookings = Booking.objects.filter(name=name, phone_number=phone_number)
        for booking in bookings:
            booking.fee = booking.land * booking.equipment.rate
        eqp=Equipment.objects.all()
        return render(request, 'user.html', {'bookings': bookings,'eqp':eqp})
    
    return redirect('user')


from django.shortcuts import render, redirect
from .models import Equipment, Booking


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        
        booking = Booking.objects.get(id=booking_id)
        current_status = booking.status
        
        if current_status != new_status:
            if current_status == 'confirmed' and new_status != 'confirmed':
                # If the current status is confirmed and it changes to any other status, increment the count
                booking.equipment.number += 1
            elif current_status != 'confirmed' and new_status == 'confirmed':
                # If the current status is not confirmed and it changes to confirmed, decrement the count
                booking.equipment.number -= 1
                
            booking.equipment.save()
        
        booking.status = new_status
        booking.save()
        
        return redirect('manager')
    
    unread_bookings = Booking.objects.filter(status='pending')
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    
    return render(request, 'manager.html', {
        'unread_bookings': unread_bookings,
        'confirmed_bookings': confirmed_bookings,
    })

@login_required(login_url='login')
@user_passes_test(is_admin)
def admins(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        
        # Assuming you have proper error handling for invalid inputs
        help_request = HelpRequest.objects.get(id=booking_id)
        help_request.status = 'Resolved' 
        help_request.save()

        return redirect('admins')  
    help_requests = HelpRequest.objects.filter(status='New')
    return render(request,'admin.html',{'help_requests': help_requests})