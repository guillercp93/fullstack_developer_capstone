"""URL Configuration for the Car Dealership Application.

This module defines the URL patterns for the djangoapp application, handling both API endpoints
and static file serving. It includes routes for user authentication, car and dealer management,
and the review system.

URL Patterns:
    Authentication:
        - /login: User login endpoint
        - /logout: User logout endpoint
        - /register: New user registration endpoint

    Car Management:
        - /get_cars: Retrieve all car makes and models
            Returns comprehensive car information including make details and associated models

    Dealer Management:
        - /get_dealers: List all dealerships
        - /get_dealers/<str:state>: Filter dealerships by state
        - /get_dealer/<int:dealer_id>: Get detailed information for a specific dealer

    Review System:
        - /reviews/dealer/<int:dealer_id>: Get all reviews for a specific dealer
        - /add_review: Submit a new dealer review (requires authentication)
            Includes sentiment analysis through IBM Cloud integration

Note:
    - All paths are prefixed with 'djangoapp/' due to the app_name setting
    - Static and media files are served using Django's static file handling in development
    - Authentication is required for submitting reviews
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "djangoapp"
urlpatterns = [
    # Authentication endpoints
    path(route="login", view=views.login_user, name="login"),
    path(route="logout", view=views.logout_request, name="logout"),
    path(route="register", view=views.registration, name="register"),
    # Car management endpoints
    path(route="get_cars", view=views.get_cars, name="get_cars"),
    # Dealer management endpoints
    path(route="get_dealers", view=views.get_dealerships, name="get_dealers"),
    path(
        route="get_dealers/<str:state>",
        view=views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path(
        route="get_dealer/<int:dealer_id>",
        view=views.get_dealer_details,
        name="get_dealer_details",
    ),
    # Review system endpoints with sentiment analysis
    path(
        route="reviews/dealer/<int:dealer_id>",
        view=views.get_dealer_reviews,
        name="get_dealer_reviews",
    ),
    path(route="add_review", view=views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
