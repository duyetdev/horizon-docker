from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard.dashboards.docker.autoscaling import api
docker_driver = api.DockerDriver()

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("docker/autoscaling/_detail_overview.html")

    def get_context_data(self, request):
        return {"is_superuser": request.user.is_superuser}

class LogTab(tabs.Tab):
    name = _("Log")
    slug = "log"
    template_name = "docker/autoscaling/_detail_log.html"
    preload = False

    def get_context_data(self, request):
    	print '=================== self.tab_group.kwargs', self.tab_group.kwargs
        instance_id = self.tab_group.kwargs['instance_id']
        try:
        	# get log for instance_id
        	data = docker_driver.container_log(instance_id)
        except Exception:
            data = _('Unable to get log for autoscaling "%s".') % instance_id
            exceptions.handle(request, ignore=True)
        return {"instance_id": instance_id,
                "console_log": data}

class ContainerDetailTabs(tabs.TabGroup):
    slug = "details"
    tabs = (OverviewTab, LogTab)
    sticky = True
