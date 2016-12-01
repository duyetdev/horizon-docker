from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.docker.autoscaling import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_container/$', views.CreateContainerView.as_view(), name='create_container'),
    # url(r'^(?P<instance_id>[^/]+)/detail/$', views.ContainerDetailView.as_view(), name='container_detail'),
)