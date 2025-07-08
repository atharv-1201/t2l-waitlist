from django.contrib import admin
from django.urls import path, include
from waitlist import views
from waitlist.views import welcome_message

urlpatterns = [
    path('', welcome_message, name='welcome'),  
    path('admin/', admin.site.urls),
    path('api/', include('waitlist.urls')),
    path('api/welcome/', views.welcome_message, name='welcome_message'),
]