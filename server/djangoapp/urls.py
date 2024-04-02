from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import static_view, about, contact

app_name = 'djangoapp'
urlpatterns = [
    path('static', static_view, name='static_view'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)