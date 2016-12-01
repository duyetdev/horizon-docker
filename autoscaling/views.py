from horizon import views
from openstack_dashboard.dashboards.docker.autoscaling import forms as project_forms
from openstack_dashboard.dashboards.docker.autoscaling import tables as project_tables
from openstack_dashboard.dashboards.docker.autoscaling import tabs as project_tabs
from openstack_dashboard.dashboards.docker.autoscaling import models as project_models

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms
from horizon import tables

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.docker.autoscaling import api
docker_driver = api.DockerDriver()

class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = project_tables.ScalingRuleTable
    template_name = 'docker/autoscaling/index.html'

    def get_data(self):
        list_instances = []

        list_instances.append(project_models.ScalingRuleItem(metric='CPU', upper_threshold='90', lower_threshold='30', node_up=2, node_down=1))
        list_instances.append(project_models.ScalingRuleItem(metric='Mem', upper_threshold='85', lower_threshold='25', node_up=3, node_down=2))

        # Add data to the context here...
        return list_instances

class CreateContainerView(forms.ModalFormView):
    form_class = project_forms.CreateContainer
    template_name = 'docker/autoscaling/create_container.html'
    modal_id = "create_container_modal"
    modal_header = _("Create Container")
    submit_label = _("Create Cotainer")	
    success_url = reverse_lazy('horizon:docker:autoscaling:index')

# class ContainerDetailView(tabs.TabView):
#     tab_group_class = project_tabs.ContainerDetailTabs
#     template_name = 'horizon/common/_detail.html'
#     success_url = reverse_lazy("horizon:docker:instance:container_detail")
#     redirect_url = reverse_lazy("horizon:docker:instance:index")
    
#     @memoized.memoized_method
#     def get_container(self):
#         try:
#             return docker_driver.get_container(self.kwargs["instance_id"])
#         except Exception:
#             exceptions.handle(self.request,
#                               _("Unable to retrieve container ~~~"))

#     def get_initial(self):
#         return {"instance_id": self.kwargs["instance_id"]}

#     def get_context_data(self, **kwargs):
#         context = super(ContainerDetailView, self).get_context_data(**kwargs)
#         instance_id = self.kwargs['instance_id']
#         context['instance_id'] = instance_id
#         context['test_duyetdev'] = True
#         # context['container'] = self.get_container()
#         # context['instance'] = context['container']
#         # context['submit_url'] = reverse(self.submit_url, args=[instance_id])
#         return context

    # def _get_actions(self, instance):
    #     table = project_tables.InstancesTable(self.request)
    #     return table.render_row_actions(instance)
