from django.urls import path

from djangoRestWorkshop.todo_auth.views import RegisterView, LoginView, LogoutView, TestUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test/', TestUser.as_view()),
]
