"""
Django views for the Car Dealership application.

This module contains view functions to handle various HTTP requests for the car dealership
application. It includes functionality for user authentication (login, logout, registration),
car inventory management, and dealership information retrieval.

The views interact with both the local database through Django models and an external
backend service through REST API calls.
"""

import json
import logging

from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangoapp.models import CarMake, CarModel
from djangoapp.populate import initiate
from djangoapp.restapis import get_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """
    Handle user login requests.

    Processes POST requests containing user credentials and authenticates the user.
    CSRF protection is disabled for this view to allow external requests.

    Args:
        request: HTTP request object containing user credentials in POST data

    Returns:
        JsonResponse: Response containing success status or error message
            Success: {"userName": username, "status": "Authenticated"}
            Error: {"error": error_message}
    """
    try:
        # Get username and password from request.POST dictionary
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        data = {"userName": username}
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data, safe=True)
    except:
        logger.error("Failed to login user")
        return JsonResponse({"error": "Login failed"}, status=500)


def logout_request(request):
    """
    Handle user logout requests.

    Logs out the currently authenticated user and cleans up their session.

    Args:
        request: HTTP request object with user information

    Returns:
        JsonResponse: Response indicating logout status
            Success: {"userName": username}
            Error: {"error": error_message}
    """
    try:
        data = {"userName": request.user.username}
        logout(request)
        logger.info(f"User {data['userName']} logged out successfully")
        return JsonResponse(data, safe=True)
    except Exception as e:
        logger.error(f"Failed to logout user: {str(e)}")
        return JsonResponse({"error": "Logout failed"}, status=500)


@csrf_exempt
def registration(request):
    """
    Handle new user registration.

    Processes POST requests containing new user information and creates a user account.
    CSRF protection is disabled to allow external requests.

    Args:
        request: HTTP request object containing user registration data in POST

    Returns:
        JsonResponse: Response indicating registration status
            Success: {"userName": username, "status": "Registered"}
            Error: {"error": error_message}
    """
    if request.method == "POST":
        data = json.loads(request.body)
        userName = data["userName"]
        password = data["password"]
        email = data["email"]
        firstName = data["firstName"]
        lastName = data["lastName"]
        user_exists = User.objects.filter(username=userName).exists()
        if user_exists:
            logger.error(f"User {userName} already exists")
            return JsonResponse({"error": "User already exists"}, status=400)
        try:
            user = User.objects.create_user(
                username=userName,
                password=password,
                email=email,
                first_name=firstName,
                last_name=lastName,
            )
            login(request, user)
            logger.info(f"User {userName} registered successfully")
            return JsonResponse(
                {"userName": userName, "status": "Registered"}, safe=True
            )
        except Exception as e:
            logger.error(f"Failed to register user: {str(e)}")
            return JsonResponse({"error": "Registration failed"}, status=500)


def get_cars(request):
    """
    Retrieve all cars from the database.

    If the database is empty, it will be populated with initial data using
    the initiate() function. Returns a list of cars with their make and model
    information.

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: List of cars with their details
            Format: {
                "CarModels": [
                    {
                        "CarModel": model_name,
                        "CarMake": make_name
                    },
                    ...
                ]
            }
    """
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("maker")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.maker.name})

    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """
    Fetch dealerships from the backend API, optionally filtered by state.

    Makes a request to the backend service to retrieve dealership information.
    Can filter dealerships by state if specified.

    Args:
        request: HTTP request object
        state (str): State to filter dealerships by. Defaults to 'All' for all dealerships.

    Returns:
        JsonResponse: JSON object containing status and dealerships data
            Success: {"status": 200, "dealers": dealerships_data}
            Error: {"error": error_message}
    """
    try:
        # Construct endpoint based on state parameter
        endpoint = "fetchDealers"
        if state != "All":
            endpoint = f"{endpoint}/{state}"

        # Get dealerships from backend
        dealerships = get_request(endpoint)

        if dealerships is None:
            logger.error("Failed to fetch dealerships from backend")
            return JsonResponse({"error": "Failed to fetch dealerships"}, status=500)

        return JsonResponse({"status": 200, "dealers": dealerships})

    except Exception as e:
        logger.error(f"Error in get_dealerships: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


def get_dealer_reviews(request, dealer_id):
    """
    Fetch reviews for a specific dealer from the backend API.

    Makes a request to the backend service to retrieve all reviews
    associated with the given dealer ID.

    Args:
        request: HTTP request object
        dealer_id (str): ID of the dealer to fetch reviews for

    Returns:
        JsonResponse: JSON object containing dealer reviews
            Success: {"status": 200, "reviews": reviews_data}
            Error: {"error": error_message}
    """
    try:
        # Construct endpoint for dealer reviews
        endpoint = f"fetchReviews/{dealer_id}"
        
        # Get reviews from backend
        reviews = get_request(endpoint)
        
        if reviews is None:
            logger.error(f"Failed to fetch reviews for dealer {dealer_id}")
            return JsonResponse({"error": "Failed to fetch dealer reviews"}, status=500)

        return JsonResponse({"status": 200, "reviews": reviews})

    except Exception as e:
        logger.error(f"Error in get_dealer_reviews: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
