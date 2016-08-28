from django.shortcuts import render, redirect
from models import Users

# Create your views here.
def index(request):
    if not 'errors' in request.session:
        request.session['errors'] = []
    return render(request, 'login_display/index.html')

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
    return render(request, 'login_display/success.html')

def register(request):
    if request.method == "POST":
        result = Users.login_mgr.register(request)
        if result[0] == False:
            print result[1]
            request.session['errors'] = result[1]
            return redirect('/')
        elif result[0] == True:
            request.session.pop('errors')
            print result[1]
            return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['user'] = {
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect('/success')

def logout(request):
    request.session.pop('user')
    return redirect('/')
