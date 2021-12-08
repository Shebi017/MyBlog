from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name="index"),
    path('detail/<int:pk>/',views.detail,name="detail"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.userLogin,name="login"),
]