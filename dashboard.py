from django.utils.translation import ugettext_lazy as _

import horizon


class DockerDashboardGroup(horizon.PanelGroup):
	slug = "autoscaling-group"
	name = _("Auto Scaling Group")
	panels = ('autoscaling', 'monitor',)

class DockerDashboard(horizon.Dashboard):
	name = _("Container")
	slug = "container"
	panels = (DockerDashboardGroup,)
	default_panel = 'autoscaling'

	def can_access(self, context):
		return True

horizon.register(DockerDashboard)