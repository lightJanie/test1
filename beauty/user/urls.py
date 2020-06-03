from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.Users.as_view()),
    url(r'^/activation$',views.ActiveView.as_view()),
    url(r'^/(?P<username>[\w]{1,20}/address$)',views.AddressView.as_view()),
    url(r'^/(?P<username>[\w]{1,20})/address/(?P<id>[\d]{1,5})$',views.AddressView.as_view()),
    url(r'^/(?P<username>[\w]{1,20})/address/default$', views.DefaultAddressView.as_view()),

]