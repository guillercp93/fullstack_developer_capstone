from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "djangoapp"
urlpatterns = [
    # # path for registration
    # path for login
    path(route="login", view=views.login_user, name="login"),
    # path for logout
    path(route="logout", view=views.logout_request, name="logout"),
    # path for registration
    path(route="register", view=views.registration, name="register"),
    # path for get cars
    path(route="get_cars", view=views.get_cars, name="get_cars"),
    # path for dealers view
    path(route="get_dealers", view=views.get_dealerships, name="get_dealers"),
    path(
        route="get_dealers/<str:state>",
        view=views.get_dealerships,
        name="get_dealers_by_state",
    ),
    # path for dealer reviews view
    # path for add a review view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
