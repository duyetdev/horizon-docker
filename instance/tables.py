from django.utils.translation import ugettext_lazy as _

from horizon import tables

class CreateContainerAction(tables.LinkAction):
    name = "container"
    verbose_name = _("Create Container")
    url = "horizon:docker:instance:create_container"
    classes = ("ajax-modal",)
    icon = "camera"

    def allowed(self, request, instance=None):
        return True
        # return instance.status in ("ACTIVE") \
        #     and not is_deleting(instance)


class MyFilterAction(tables.FilterAction):
    name = "dockerfilter"


class InstancesTable(tables.DataTable):
    container_id = tables.Column("instance_id", verbose_name=_("ID"))
    container_name = tables.Column("name", verbose_name=_("Name"))
    container_status = tables.Column('status', verbose_name=_("Status"))
    container_ip = tables.Column('ip', verbose_name=_("IP"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
        row_actions = (CreateContainerAction,)