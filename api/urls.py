from django.urls import path, include

from api import views

urlpatterns = [
    path('listing/', include([
        path('', views.ListingsView.as_view()),
        path('<int:pk>/', views.ListingsRetrieveView.as_view()),
        path('<int:pk>/rooms/', views.ProfileList.as_view()),
    ])),
    path('room/', include([
        path('', views.RoomsView.as_view()),
        path('<int:pk>/', views.RoomsRetrieveView.as_view()),
    ])),
    path('reservation/', include([
        path('', views.ReservationsView.as_view()),
        path('<int:pk>/', views.ReservationsRetrieveView.as_view()),
    ])),
    path('check/', views.check_rooms),
]
