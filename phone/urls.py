from django.conf.urls import url
from .views import index,details,manager,delete,login,register,logout

urlpatterns = [
    url(r'^index/$', index),
    url(r'^(?P<product_id>\d+)/', details),
    url(r'^manager/', manager),
    url(r'^delete/', delete),
    url(r'^login/', login),
    url(r'^register/', register),
    url(r'^logout/',logout),
]