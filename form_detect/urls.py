from django.urls import path,  include
from form_detect.views import index

urlpatterns = [
    path('f_name1=<str:value_1>&f_name2=<str:value_2>', index)
]