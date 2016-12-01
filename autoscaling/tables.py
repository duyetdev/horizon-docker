from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard import policy

class RuleFilterAction(tables.FilterAction):
    name = "rulefilter"

class StopContainerAction(tables.LinkAction):
    name = "stop_container"
    verbose_name = _("Stop")
    url = "horizon:docker:autoscaling:stop_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("running")

class AddRuleAction(tables.LinkAction):
    name = "add_rule"
    verbose_name = _("Add rule")
    url = "horizon:container:autoscaling:add_rule"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return True

class DeleteRuleAction(tables.LinkAction):
    name = "delete_rule"
    verbose_name = _("Delete rule")
    url = "horizon:container:autoscaling:delete_rule"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return True

class RemoveContainerAction(tables.LinkAction):
    name = "remove_container"
    verbose_name = _("Delete")
    url = "horizon:docker:autoscaling:delete_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("exited", "running")

class ScalingRuleTable(tables.DataTable):
    metric = tables.Column('metric', verbose_name=_("Metric"))
    upper_threshold = tables.Column('upper_threshold', verbose_name=_("Upper threshold"))
    lower_threshold = tables.Column('lower_threshold', verbose_name=_("Lower threshold"))
    node_up = tables.Column('node_up', verbose_name=_("Node up"))
    node_down = tables.Column('node_down', verbose_name=_("Node down"))

    class Meta:
        name = "scaling-rules"
        verbose_name = _("Scaling Rules")
        table_actions = (RuleFilterAction, AddRuleAction, DeleteRuleAction )
        row_actions = (DeleteRuleAction, )