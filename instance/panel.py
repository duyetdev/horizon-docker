from django.utils.translation import ugettext_lazy as _
import horizon
from openstack_dashboard.dashboards.docker import dashboard


class DockerInstancePanel(horizon.Panel):
    name = _("Instance")
    slug = "instance"


dashboard.DockerDashboard.register(DockerInstancePanel)