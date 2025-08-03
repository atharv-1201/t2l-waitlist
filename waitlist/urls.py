from django.urls import path
from .views import WaitlistSignupView, debug_database


urlpatterns = [
    path('signup/', WaitlistSignupView.as_view(), name='waitlist-signup'),
    path('debug/', debug_database, name='debug-database'),
]