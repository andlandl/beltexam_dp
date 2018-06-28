from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^wish_items/(?P<product_id>\d+)$', views.wish_items),
    url(r'^wish/(?P<wishitem_id>\d+)$', views.wish),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^removewish/(?P<wanter_id>\d+)$', views.removewish),
    url(r'^logout$', views.logout)
]
