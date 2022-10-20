from django.urls import path
from . import views
from Hello_Buddy.views import reverse_to_home
urlpatterns = [
    path('', reverse_to_home),
    path('home',views.home, name='home'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('profile-user', views.profile_user, name='profile-user')
]
