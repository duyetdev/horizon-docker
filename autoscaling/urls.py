from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.docker.autoscaling import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_rule/$', views.AddRuleView.as_view(), name='add_rule'),
    url(r'^(?P<rule_id>[^/]+)delete_rule/$', views.DeleteRuleView.as_view(), name='delete_rule'),
)