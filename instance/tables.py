from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard import policy

class CreateContainerAction(tables.LinkAction):
    name = "container"
    verbose_name = _("Create Container")
    url = "horizon:docker:instance:create_container"
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
    url = "horizon:docker:instance:stop_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("running")

class RemoveContainerAction(tables.LinkAction):
    name = "remove_container"
    verbose_name = _("Delete")
    url = "horizon:docker:instance:delete_container"
    classes = ("ajax-modal", "btn",)

    def allowed(self, request, instance=None):
        return instance.status in ("exited", "running")

class InstancesTable(tables.DataTable):
    container_id = tables.Column("container_id", verbose_name=_("Instance ID"))
    container_image = tables.Column("image", verbose_name=_("IMAGE"))
    container_status = tables.Column('status', verbose_name=_("Status"))
    container_ip = tables.Column('ip', verbose_name=_("IP"))
    container_port = tables.Column('port', verbose_name=_("Ports"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction, CreateContainerAction, )
        # table_actions_menu = (CreateContainerAction, )
        row_actions = (StopContainerAction, RemoveContainerAction, )
        