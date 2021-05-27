from django.urls import path
from . import views

urlpatterns = [
    path('travel/home', views.home),
    path('travel/add', views.add, name='add'),
    path('travel/create', views.create, name='create'),
    path('travel/destination/<int:trip_id>', views.show),
    path('travel/join/<int:trip_id>', views.join),
    path('travel/logout', views.logout),
]