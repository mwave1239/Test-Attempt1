from django.shortcuts import render, redirect
from . import models
from models import Users, Trips

def index(request):
    if not 'errors' in request.session:
        request.session['errors'] = []
    return render(request, 'belt_display/index.html')

def login(request):
    if request.method == "POST":
        login = Users.login_mgr.valid_login(request)
        if login[0] == False:
            request.session['errors'] = login[1]
            return redirect('/')
        elif login[0] == True:
            request.session.pop('errors')
            print login[1]
            return log_user_in(request, login[1])

def success(request):
    if not 'user' in request.session:
        return redirect('/')
    return redirect('/travels')

def register(request):
    if request.method == "POST":
        result = Users.login_mgr.register(request)
        if result[0] == False:
            print result[1]
            request.session['errors'] = result[1]
            return redirect('/')
        elif result[0] == True:
            # request.session.pop('errors')
            print result[1]
            return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['user'] = {
        'id': user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect('/success')

def logout(request):
    request.session.pop('user')
    return redirect('/')

def travels(requet):
    trips = Trips.objects.filter()
    email = request.session['email']
    user = Users.objects.get(email=email)
    user_id = user.id
    trips = Trips.objects.filter(user_created=user)
    trips_user = Trips.objects.all()
    join_trip = Trip.objects.filter(users=user)
    context = {
        'user_trips': trips,
        'joined_trip': join_trip,
        'trips_user': trips_user,
        'user': user,
    }
    return render(request, 'belt_display/user_trips.html', context)

def add_trip(request):
    return render(request, 'belt_display/add.html')

def create_trip(request):
    if request.method == "POST":
        trip = Trips.trip_mgr.trip_valid(user_created=request.session['email'], destination=request.POST['destination'], description=request.POST['description'], date_start=request.POST['date_start'], date_to=request.POST['date_to'])
        if trip[0] == False:
            request.session['errors'] = trip[1]
            return redirect('/travels')
        elif trip[0] == True:
            print trip[1]
            return redirect('/travels')

def show_trip(request, id):
    trips = Trips.object.get(id=id)
    users = trips.Users.all()
    print users
    context = {
        'trip' : trips,
        'users': users,
    }
    return render(request, "belt_display/show_trip.html", context)

def join_trip(request, id):
    name =request.session['user']
    user = Users.objects.get(name=name)
    add_user_trip = Trips.objects.get(id=id)
    add_user_trip.Users.add(user)
    add_user_trip.save()
    return redirect('/travels')
