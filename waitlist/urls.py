from django.urls import path
from .views import WaitlistSignupView

urlpatterns = [
    path('signup/', WaitlistSignupView.as_view(), name='waitlist-signup'),
]