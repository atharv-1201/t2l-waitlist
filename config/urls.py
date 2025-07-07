from django.contrib import admin
from django.urls import path, include
from waitlist.views import welcome_message

urlpatterns = [
    path('', welcome_message, name='welcome'), 
    path('admin/', admin.site.urls),
    path('api/', include('waitlist.urls')),
]