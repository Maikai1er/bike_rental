from django.urls import path
from . import views

urlpatterns = [
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('bikes/', views.BikeListView.as_view(), name='bike-list'),
    path('rentals/create/', views.RentalCreateView.as_view(), name='rental-create'),
    path('rentals/return/<int:pk>/', views.RentalReturnView.as_view(), name='rental-return'),
    path('users/rentals/', views.UserRentalHistoryView.as_view(), name='user-rental-history'),
]
