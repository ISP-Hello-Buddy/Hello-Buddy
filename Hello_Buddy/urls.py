from django.urls import path
from . import views
from Hello_Buddy.views import event, reverse_to_home
urlpatterns = [
    path('', reverse_to_home),
    path('home',views.home, name='home'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('create', views.create, name='create'),
    path('event/<int:event_id>', views.event, name='event'),
    path('<str:event_category>/', views.events_by_category, name='event_category'),
]
