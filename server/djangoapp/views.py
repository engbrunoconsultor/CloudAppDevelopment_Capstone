from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def static_view(request):
    return render(request, 'djangoapp/static_template.html')

def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact_us.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp', context)
    
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp")
        else:
            return render(request, 'djangoapp/user_registration.html', context)
    

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    # context = {}
    # if request.method == "GET":
    #     return render(request, 'djangoapp/dealership.html', context)
    try:
        # Fetch all dealership records
        dealerships = CarDealer.objects.all()
        if not dealerships:
            return JsonResponse({'error': '404: The database is empty'}, status=404)
        
        # Serialize data to JSON format
        dealerships_data = list(dealerships.values('id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long'))
        return JsonResponse(dealerships_data, safe=False)
    except Exception as e:
        # Log the exception
        return JsonResponse({'error': '500: Something went wrong on the server', 'details': str(e)}, status=500)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealerships_by_state(request):
    state_abbr = request.GET.get('state', '')
    if state_abbr:
        dealers = list(CarDealer.objects.filter(st=state_abbr).values())
        if not dealers:
            return JsonResponse({'error': '404: The state does not exist'}, status=404)
        return JsonResponse(dealers, safe=False)
    return JsonResponse({'error': '400: State parameter is missing'}, status=400)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def get_reviews_by_dealership(request):
    dealer_id = request.GET.get('dealerId', '')
    if not dealer_id:
        return JsonResponse({'error': '400: dealerId parameter is missing'}, status=400)

    try:
        dealership = CarDealer.objects.get(pk=dealer_id)
        reviews = Review.objects.filter(dealership=dealership)
        if not reviews:
            return JsonResponse({'error': '404: No reviews found for this dealership'}, status=404)
        
        reviews_data = list(reviews.values(
            'id', 'name', 'dealership_id', 'review', 'purchase',
            'purchase_date', 'car_make', 'car_model', 'car_year'))
        
        return JsonResponse(reviews_data, safe=False)
    except CarDealer.DoesNotExist:
        return JsonResponse({'error': '404: dealerId does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': '500: Something went wrong on the server', 'details': str(e)}, status=500)

@csrf_exempt  # Disable CSRF token for demonstration purposes
@require_http_methods(["POST"])  # Only accept POST requests
def post_review(request):
    try:
        # Parse the JSON body of the request
        review_data = json.loads(request.body)
        review_info = review_data.get('review', {})

        # Validate the existence of the dealership
        dealership_id = review_info.get('dealership')
        if not CarDealer.objects.filter(id=dealership_id).exists():
            return JsonResponse({'error': '404: Dealership not found'}, status=404)

        # Create and save the new review object
        review = Review(
            name=review_info['name'],
            dealership_id=dealership_id,
            review=review_info['review'],
            purchase=review_info['purchase'],
            purchase_date=review_info.get('purchase_date'),
            car_make=review_info.get('car_make'),
            car_model=review_info.get('car_model'),
            car_year=review_info.get('car_year')
        )
        review.save()

        # Return the created review
        return JsonResponse({
            'id': review.id,
            'name': review.name,
            'dealership': review.dealership_id,
            'review': review.review,
            'purchase': review.purchase,
            'purchase_date': review.purchase_date,
            'car_make': review.car_make,
            'car_model': review.car_model,
            'car_year': review.car_year
        })
    except KeyError as e:
        # If a required field is missing
        return JsonResponse({'error': f'400: Missing field {str(e)}'}, status=400)
    except Exception as e:
        # Log the error and return a generic server error response
        return JsonResponse({'error': '500: Something went wrong on the server', 'details': str(e)}, status=500)