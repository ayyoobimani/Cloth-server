from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest import views

urlpatterns = patterns('',
                       url(r'^images[/]?$', views.getImages, name='getImages'),
                       url(r'^action[/]?$', views.doAction, name='doAction'),
                       url(r'^getTags[/]?$', views.getAllOfTags, name='getTag'),
)
