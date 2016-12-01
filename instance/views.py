from horizon import views
from openstack_dashboard.dashboards.docker.instance import forms as project_forms
from openstack_dashboard.dashboards.docker.instance import tables as project_tables
from openstack_dashboard.dashboards.docker.instance import tabs as project_tabs

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms
from horizon import tables

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.docker.instance import api
docker_driver = api.DockerDriver()

class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = project_tables.InstancesTable
    template_name = 'docker/instance/index.html'

    def get_data(self):
    	list_instances = docker_driver.list_instances_table()

        # Add data to the context here...
        return list_instances

class CreateContainerView(forms.ModalFormView):
    form_class = project_forms.CreateContainer
    template_name = 'docker/instance/create_container.html'
    modal_id = "create_container_modal"
    modal_header = _("Create Container")
    submit_label = _("Create Cotainer")	
    success_url = reverse_lazy('horizon:docker:instance:index')


class ContainerDetailView(tabs.TabView):
    tab_group_class = project_tabs.ContainerDetailTabs
    template_name = 'horizon/common/_detail.html'
    success_url = reverse_lazy("horizon:docker:instance:container_detail")
    redirect_url = reverse_lazy("horizon:docker:instance:index")
    
    @memoized.memoized_method
    def get_container(self):
        try:
            return docker_driver.get_container(self.kwargs["instance_id"])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve container ~~~"))

    def get_initial(self):
        return {"instance_id": self.kwargs["instance_id"]}

    def get_context_data(self, **kwargs):
        context = super(ContainerDetailView, self).get_context_data(**kwargs)
        instance_id = self.kwargs['instance_id']
        context['instance_id'] = instance_id
        context['test_duyetdev'] = True
        # context['container'] = self.get_container()
        # context['instance'] = context['container']
        # context['submit_url'] = reverse(self.submit_url, args=[instance_id])
        return context

    # def _get_actions(self, instance):
    #     table = project_tables.InstancesTable(self.request)
    #     return table.render_row_actions(instance)
