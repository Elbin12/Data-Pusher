from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('account/create/', views.AccountView.as_view()),
    path('account/list/', views.AccountList.as_view()),
    path('account/update/<int:id>/', views.AccountUpdate.as_view()),
]