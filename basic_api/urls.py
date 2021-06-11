from django.urls import path
from .views import RegisterUser, BlacklistToken

urlpatterns = [
    path('register/', RegisterUser.as_view(),name="register"),
    path('logout/blacklist/', BlacklistToken.as_view(),name="blacklist")
]
