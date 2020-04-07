import datetime
from dateutil import relativedelta
from django.template import loader
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

from .models import Product, Locality, Listing, CustomUser, Subscription

################################################################################################################################################

def index(request):
    return render(request, 'index.html')

################################################################################################################################################

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
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
        listings = Listing.objects.all().filter(locality=locality.id)
        listings.count = len(listings)
        listing_list = list(listings)
        return render(request, 'view_locality.html', {"locality" : locality, "listings" : listings})
    else:
        return redirect('/')

################################################################################################################################################

def purchase(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST.get('id', '')
            locality_id = request.POST.get('locality_id', '')
            submit_form = request.POST.get('submit_form', '')

            if len(id) > 0:
                if Listing.objects.filter(id=id).exists():
                    is_form_submitted = request.POST.get('submit_form', '')

                    current_user = request.user
                    userobj = CustomUser.objects.get(id=current_user.id)
                    listing_info = Listing.objects.get(id=id)
                    product_info = Product.objects.get(name__exact=listing_info.name)
                    locality_info = Locality.objects.get(id=locality_id)

                    if is_form_submitted == "true":
                        address_1 = request.POST.get('address_1', '')
                        address_2 = request.POST.get('address_2', '')
                        timing = request.POST.get('timing', '')
                        mobile = request.POST.get('mobile', '')
                        payment_type = request.POST.get('payment_type', '')
                        subscription_duration = request.POST.get('subscription_duration', '')
                        total_amount = request.POST.get('total_amount', '')
                        duration_from = datetime.date.today() + relativedelta.relativedelta(months=0)
                        duration_till = datetime.date.today() + relativedelta.relativedelta(months=int(subscription_duration))
                        #duration = "2020-05-01"


                        if len(address_1) == 0:
                            messages.error(request, 'Please enter a valid first address!')
                            return render(request, 'purchase.html', {"listing_info" : listing_info, "userobj" : userobj})

                        if len(address_2) == 0:
                            messages.error(request, 'Please enter a valid second address!')
                            return render(request, 'purchase.html', {"listing_info" : listing_info, "userobj" : userobj})

                        if len(timing) == 0:
                            messages.error(request, 'Please enter a valid timing!')
                            return render(request, 'purchase.html', {"listing_info" : listing_info, "userobj" : userobj})

                        if len(mobile) == 0:
                            messages.error(request, 'Please enter a valid mobile number!')
                            return render(request, 'purchase.html', {"listing_info" : listing_info, "userobj" : userobj})

                        #if len(payment_type) == 0:
                            #messages.error(request, 'Please enter a valid payment type!')
                            #return render(request, 'purchase.html', {"listing_info" : listing_info, "userobj" : userobj})

                        subscription = Subscription.objects.create(seller=listing_info.seller, buyer=userobj, product=product_info, price=listing_info.price, timing=timing, duration_from=duration_from, duration_till=duration_till, total_amount=total_amount, address_1=address_1, address_2=address_2, locality=locality_info, mobile=mobile)
                        subscription.save()

                        userobj.account_balance -= float(total_amount)
                        userobj.save()

                        return render(request, 'purchase.html', {"paid" : "true"})
                    else:
                        listing_info.locality_id = locality_id
                        return render(request, 'purchase.html', {"paid" : "false", "listing_info" : listing_info, "userobj" : userobj})
            else:
                return redirect('/')
        else:
            return redirect('/localities')
    else:
        return redirect('/login')

################################################################################################################################################

def profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.user_type == 1:
            subscriptions = Subscription.objects.all().filter(buyer=current_user.id)
            subscriptions_count = Subscription.objects.all().filter(buyer=current_user.id).count()
            return render(request, 'profile.html', {"subscriptions" : subscriptions, "subscriptions_count" : subscriptions_count})
        else:
            subscriptions = Subscription.objects.all().filter(seller=current_user.id)
            subscriptions_count = Subscription.objects.all().filter(seller=current_user.id).count()

            listings = Listing.objects.all().filter(seller=current_user.id)
            listings_count = Listing.objects.all().filter(seller=current_user.id).count()

            return render(request, 'profile.html', {"subscriptions" : subscriptions, "subscriptions_count": subscriptions_count, "listings" : listings, "listings_count" : listings_count})

    else:
        return redirect("/")

################################################################################################################################################

def create_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user
            product = request.POST.get('product', '')
            price = request.POST.get('price', '')
            localities = request.POST.getlist('localities[]', '')

            listing = Listing.objects.create(price=price, name=Product.objects.get(id__exact=product), seller=CustomUser.objects.get(id=current_user.id))
            for each_locality in localities:
                listing.locality.add(Locality.objects.get(id__exact=each_locality))
            listing.save()

            return redirect("/profile")
        else:
            products = Product.objects.all()
            localities = Locality.objects.all()
            return render(request, 'create-listing.html', {"success" : "false", "products" : products, "localities" : localities})
    else:
        return redirect("/")

################################################################################################################################################

def delete_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            listing_id = int(request.POST.get('id', ''))
            if listing_id > 0:
                action_completed = request.POST.get('action_completed', '')
                if (len(action_completed) > 0) and (action_completed == "true"):
                    if Listing.objects.filter(id=listing_id).exists():
                        current_user = request.user
                        user_type = current_user.user_type
                        if user_type == 2:
                            listing = Listing.objects.get(id__exact=listing_id)
                            if(listing.seller == current_user):
                                listing.delete()
                                return redirect("/profile")
                            else:
                                messages.error(request, 'Error!')
                                return render(request, 'delete-listing.html', {"id" : listing_id})
                        else:
                            return redirect("/profile")
                    else:
                        return redirect("/profile")
                else:
                    return render(request, 'delete-listing.html', {"id" : listing_id})
            else:
                return redirect("/profile")
        else:
            return redirect("/profile")
    else:
        return redirect("/login")

################################################################################################################################################

def add_money(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_type = current_user.user_type
        if user_type == 1:
            if request.method == "POST":
                amount = float(request.POST.get('amount', ''))
                if amount > 0:
                    User = CustomUser.objects.get(id=current_user.id)
                    User.account_balance += amount
                    User.save()
                    return redirect("/profile")
                else:
                    return redirect("/profile/add-money")
            else:
                return render(request, 'add-money.html')
        else:
            return redirect("/")
    else:
        return redirect("/login")

################################################################################################################################################

def create_account(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            account_type = int(request.POST.get('account_type', ''))
            account_balance = 0
            if account_type == 1:
                account_balance = 1500.0
            else:
                account_balance = 0

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
                            user = User.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name, user_type=account_type, account_balance=account_balance)
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
