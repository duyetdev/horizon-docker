from django.utils.translation import ugettext_lazy as _
import horizon
from openstack_dashboard.dashboards.docker import dashboard


class DockerMonitorPanel(horizon.Panel):
    name = _("Monitor")
    slug = "monitor"


dashboard.DockerDashboard.register(DockerMonitorPanel)