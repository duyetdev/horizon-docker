from django.utils.translation import ugettext_lazy as _
import horizon
from openstack_dashboard.dashboards.docker import dashboard


class AutoScalingPanel(horizon.Panel):
    name = _("Auto Scaling")
    slug = "autoscaling"


dashboard.DockerDashboard.register(AutoScalingPanel)