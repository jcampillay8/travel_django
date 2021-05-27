from django.shortcuts import render, redirect

from .models import Trip
from ..login_register.models import User

from django.contrib import messages


# Create your views here.
def home(request):
    context = {
        'user': User.objects.get(id = request.session['id']),
        'other_users': User.objects.all().exclude(id = request.session['id']),
    }
    return render(request, 'travel/home.html', context)

def add(request):
    return render(request, 'travel/add_travel.html')

def show(request, trip_id):
    context = {
        'trip': Trip.objects.get(id = trip_id)
    }
    return render(request, 'travel/show_travel.html', context)

def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    traveler = User.objects.get(id=request.session['id'])
    traveler.trips.add(trip)
    traveler.save()

    return redirect('/travel/home')

def create(request):
    result = Trip.objects.validate_trip(request.POST, request.session['id'])

    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/travel/add')

    return redirect('/travel/home')

def logout(request):
    request.session.flush()
    return redirect('/')