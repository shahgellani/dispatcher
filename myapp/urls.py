from django.contrib import admin
from django.views.generic import TemplateView

from myapp import views

from django.urls import path, include
from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url('^Register/', views.RegisterView.as_view()),
    url('^Login/', views.LoginView.as_view()),
    url('^Hellow/', views.HelloView.as_view()),
    url('^ShowDispatches/', views.DispatchView.as_view()),
    url('^UpdateArrivalDate/', views.UpdateArrivalView.as_view()),
    url('^UpdateDepartureDate/', views.UpdateDepartureView.as_view()),

    url('^ShowDispatchesDetail/', views.ShowDispatchDetailView.as_view()),
    url('^Pod/', views.P_O_D.as_view()),
    url(r'^logout/', views.Logout.as_view()),

]
