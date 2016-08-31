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
            request.session['email'] = request.POST.getlist('email')
            return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['user'] = {
        'id': user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    request.session['email'] = user.email
    try:
        request.session.pop('errors')
    except:
        request.session['errors'] = []
    return redirect('/success')

def logout(request):
    request.session.pop('user')
    request.session.pop('email')
    return redirect('/')

def travels(request):
    print request.session['user']
    email = request.session['email']
    print email
    trips = Trips.objects.filter()
    try:
        user = Users.objects.get(email=email)
        user_id = user.id
    except:
        user = []
    try:
        trips = Trips.objects.filter(user_created=email)
    except:
        trips = []
    trips_user = Trips.objects.all()
    try:
        join_trip = Trip.objects.filter(users=user)
    except:
        join_trip = []
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
        # email = request.session['email']
        trip = Trips.trip_mgr.trip_valid(request)
        print trip
        if trip[0] == False:
            request.session['errors'] = trip[1]
            return redirect('/travels/add')
        elif trip[0] == True:
            print trip[1]
            return redirect('/travels')

def show_trip(request, id):
    trips = Trips.objects.get(id=id)
    users = trips.users.all()
    print users
    context = {
        'trip' : trips,
        'users': users,
    }
    return render(request, "belt_display/show_trip.html", context)

def join_trip(request, id):
    email =request.session['email']
    user = Users.objects.get(email=email)
    add_user_trip = Trips.objects.get(id=id)
    add_user_trip.users.add(user)

    # add_user_trip.save()
    return redirect('/travels')
