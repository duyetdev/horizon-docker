from django.utils.translation import ugettext_lazy as _

import horizon


class DockerDashboardGroup(horizon.PanelGroup):
	slug = "dockergroup"
	name = _("Docker")
	panels = ('monitor',)

class DockerDashboard(horizon.Dashboard):
	name = _("Docker")
	slug = "docker"
	panels = (DockerDashboardGroup,)
	default_panel = 'monitor'

	def can_access(self, context):
		return True

horizon.register(DockerDashboard)