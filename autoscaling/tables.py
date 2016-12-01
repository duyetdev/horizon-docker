from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard import policy

class CreateContainerAction(tables.LinkAction):
    name = "container"
    verbose_name = _("Create Container")
    url = "horizon:docker:autoscaling:create_container"
    classes = ("ajax-modal", "btn-primary", )

    # icon = "camera"

    # def allowed(self, request, instance=None):
    #     return True
        # return instance.status in ("ACTIVE") \
        #     and not is_deleting(instance)


class MyFilterAction(tables.FilterAction):
    name = "dockerfilter"

class StopContainerAction(tables.LinkAction):
    name = "stop_container"
    verbose_name = _("Stop")
    url = "horizon:docker:autoscaling:stop_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("running")

class RemoveContainerAction(tables.LinkAction):
    name = "remove_container"
    verbose_name = _("Delete")
    url = "horizon:docker:autoscaling:delete_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("exited", "running")

class InstancesTable(tables.DataTable):
    container_id = tables.Column("container_id", verbose_name=_("Instance ID"), 
        link="horizon:docker:autoscaling:container_detail")
    container_image = tables.Column("image", verbose_name=_("IMAGE"))
    container_status = tables.Column('status', verbose_name=_("Status"))
    container_startedat = tables.Column('startedat', verbose_name=_("Started at"))
    container_ip = tables.Column('ip', verbose_name=_("IP"))
    container_port = tables.Column('port', verbose_name=_("Ports"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction, CreateContainerAction, )
        # table_actions_menu = (CreateContainerAction, )
        row_actions = (StopContainerAction, RemoveContainerAction, )

class ScalingRuleTable(tables.DataTable):
    metric = tables.Column('metric', verbose_name=_("Metric"))
    upper_threshold = tables.Column('upper_threshold', verbose_name=_("Upper threshold"))
    lower_threshold = tables.Column('lower_threshold', verbose_name=_("Lower threshold"))
    node_up = tables.Column('node_up', verbose_name=_("Node up"))
    node_down = tables.Column('node_down', verbose_name=_("Node down"))

    class Meta:
        name = "scaling-rules"
        verbose_name = _("Scaling Rules")
        table_actions = (MyFilterAction, CreateContainerAction, )
        # table_actions_menu = (CreateContainerAction, )
        row_actions = (StopContainerAction, RemoveContainerAction, )