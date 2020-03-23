from django.template import loader
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required


from .models import Product, Locality, Listing

################################################################################################################################################

def index(request):
    return render(request, 'index.html')

################################################################################################################################################

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if len(email) == 0:
            messages.error(request, 'Please enter a valid email!')
            return redirect('login')
        elif len(password) == 0:
            messages.error(request, 'The password field cannot be empty!')
            return redirect('create_account')
        else:
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect('login')
    else:
        return render(request, 'login.html')

################################################################################################################################################

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

################################################################################################################################################

def localities(request):
    localities_list = Locality.objects.all()
    return render(request, 'localities.html', {"localities" : localities_list})

################################################################################################################################################

def services(request):
    products_list = Product.objects.all()
    return render(request, 'services.html', {"services" : products_list})

################################################################################################################################################

def single_locality(request, title):
    if request.method == 'GET':
        locality = Locality.objects.get(slug__iexact=title)
        print(locality.id)
        listings = Listing.objects.all().filter(locality=locality.id)
        return render(request, 'view_locality.html', {"locality" : locality, "listings" : listings})
    else:
        return redirect('/')

################################################################################################################################################

def create_account(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        account_type = int(request.POST.get('account_type', ''))

        if len(first_name) == 0:
            messages.error(request, 'First name cannot be empty!')
            return redirect('create_account')
        elif len(last_name) == 0:
            messages.error(request, 'Last name cannot be empty!')
            return redirect('create_account')
        elif len(email) == 0:
            messages.error(request, 'Please enter a valid email!')
            return redirect('create_account')
        elif len(password1) == 0:
            messages.error(request, 'Enter your password fields correctly!')
            return redirect('create_account')
        elif len(password2) == 0:
            messages.error(request, 'Enter your password fields correctly!')
            return redirect('create_account')
        else:
            if password1 == password2:
                User = get_user_model()

                if User.objects.filter(email=email).exists():
                    messages.error(request, 'An Account already exists with the same email.')
                    return redirect('create_account')
                else:
                    if account_type == 1 or account_type == 2:
                        user = User.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name, user_type=account_type)
                        user.save()

                        user = auth.authenticate(email=email, password=password1)
                        auth.login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'Please select your account type!')
                        return redirect('create_account')
            else:
                messages.error(request, 'The passwords you entered do not match!')
                return redirect('create_account')
        render(request, 'create_account.html')
    else:
        return render(request, 'create_account.html')
