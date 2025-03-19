from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),

    path('account/create/', views.AccountView.as_view()),
    path('account/list/', views.AccountList.as_view()),
    path('account/update/<int:id>/', views.AccountUpdate.as_view()),
    path('account/delete/<int:id>/', views.AccountDelete.as_view()),

    path('destination/create/', views.DestinationCreate.as_view()),
    path('destination/update/<int:id>/', views.DestinationUpdate.as_view()),
    path('destination/delete/<int:id>/', views.DestinationDelete.as_view()),

    path('server/incoming_data/', views.IncomingData.as_view()),
]