from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.docker.instance import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_container/$',
    	views.CreateContainerView.as_view(),
    	name='create_container'),
)