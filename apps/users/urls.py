from django.urls import path
from .views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]