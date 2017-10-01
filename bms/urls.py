#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??                               
#@author:   Dylan_wu                                                        
#@software:    PyCharm                  
#@file:    urls.py
#@time:    2017/8/15 11:48
#----------------------------------------------
from django.conf.urls import url
from bms import views

urlpatterns = [
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^users/(?P<id>\d*)/$', views.users),
    url(r'^authorization/(?P<id>\d*)/$', views.authorization),
    url(r'^creat_asset/', views.creat_asset),
    url(r'^del_asset/', views.del_asset),
    url(r'^del_user/', views.del_user),
    url(r'^batch_del/', views.batch_del),
    url(r'^mod_asset/(?P<id>\d*)/$', views.mod_asset),
    url(r'^bulkcreate/', views.bulk_create_models),
    url(r'^ajax/', views.do_ajax),
    url(r'^applications/terminal/', views.web_terminal),
]