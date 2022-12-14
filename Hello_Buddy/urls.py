from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.reverse_to_home, name=''),
    path('home', views.home, name='home'),
    path('aboutus', views.about_us, name='aboutus'),
    path('map', views.map, name='map'),
    path('profile-user', views.profile_user, name='profile-user'),
    path('create', views.create, name='create'),
    path('event/<int:event_id>', views.event, name='event'),
    path('<str:event_category>', views.events_by_category, name='event_category'),
    path('event/edit/<int:event_id>', views.edit, name='edit'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
