from datetime import datetime
import json
import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

# from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
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


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    try:
        data = {"userName": request.user.username}
        logout(request)
        logger.info(f"User {data['userName']} logged out successfully")
        return JsonResponse(data, safe=True)
    except Exception as e:
        logger.error(f"Failed to logout user: {str(e)}")
        return JsonResponse({"error": "Logout failed"}, status=500)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
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


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
