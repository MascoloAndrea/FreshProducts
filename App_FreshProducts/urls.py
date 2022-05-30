from django.urls import path
from django.contrib import admin
from . import views
#from django.conf.urls import url
'''
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
'''

urlpatterns = [
    path('home/', views.index, name='index'),

    path('home/contact/', views.contact, name='contact'),
    path('home/registrer/', views.registrer, name='registrer'),
    path('area_riservata/', views.area_riservata, name='area_riservata'),
    path('area_riservata/product/', views.product, name='product'),
    path('area_riservata/assistance/', views.assistance, name='assistance'),
    path('area_riservata/settings/', views.settings, name='settings'),
    path('area_riservata/product/prox_to_scadenza/', views.prox_to_scadenza, name='prox_to_scadenza'),
    path('area_riservata/catalogo/without_scadenza/', views.without_scadenza, name='without_scadenza'),
    path('area_riservata/catalogo/article_scad/', views.article_scad, name='article_scad'),
    path('area_riservata/remove_product/', views.remove_products, name='remove_products'),
    path('area_riservata/modify_product/process/', views.process_modify_prod, name='process_modify_prod'),
    path('area_riservata/modify_product/', views.modify_product, name='modify_product'),
    path('area_riservata/new_product/', views.new_product, name='new_product'),
    path('area_riservata/new_product/process/', views.process, name='process'),
    path('area_riservata/new_product/process/executed/', views.executed, name='executed'),
    path('admin/', admin.site.urls),
    path('area_riservata/area_utente/', views.area_utente, name='area_utente'),
    path('area_riservata/catalogo/', views.catalogo, name='catalogo'),
    path('area_riservata/catalogo/expiry_date/', views.expiry_date, name='expiry_date'),
    path('home/login/', views.signin, name='signin'),
    #path('home/login/process/', views.process, name='process'),
    #path('home/login/process/', views.signin, name='signin'),
    path('home/logout/', views.signout, name='signout'),
    path('error403/', views.AccessDenied, name='AccessDenied')
    #url(r'^connection/','formView', name = 'loginform'),
    #url(r'^login/', 'login', name = 'login'),
]





