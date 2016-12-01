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

class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = project_tables.ScalingRuleTable
    template_name = 'container/autoscaling/index.html'

    def get_data(self):
        list_instances = []

        list_instances.append(project_models.ScalingRuleItem(metric='CPU', upper_threshold='90', lower_threshold='30', node_up=2, node_down=1))
        list_instances.append(project_models.ScalingRuleItem(metric='Mem', upper_threshold='85', lower_threshold='25', node_up=3, node_down=2))

        # Add data to the context here...
        return list_instances

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # if hasattr(self, "table"):
        #     context[self.context_object_name] = self.table

        search_opts = {'paginate': False}
        try:
            instances, self._more = api.nova.server_list(
                self.request,
                search_opts=search_opts)
        except Exception:
            self._more = False
            instances = []
            exceptions.handle(self.request,
                              _('Unable to retrieve instances.'))
            print '====================', instances
        context['vm_list'] = []
        if instances:
            for instance in instances:
                print type(instance), '=================+++++++++++++++++++++++++'
                context['vm_list'].append({'id': instance.key_name, 'name': instance.name})

        # context['vm_list'] = ( 'vm-olp1', 'vm-olp2', 'vm-olp3' )
        context['current_vm'] = self.request.GET.get('vm', None)
        if not context['current_vm']:
            context['current_vm'] = context['vm_list'][0] \
                if len(context['vm_list']) > 0 else False


        return context

class CreateContainerView(forms.ModalFormView):
    form_class = project_forms.CreateContainer
    template_name = 'docker/autoscaling/create_container.html'
    modal_id = "create_container_modal"
    modal_header = _("Create Container")
    submit_label = _("Create Cotainer") 
    success_url = reverse_lazy('horizon:docker:autoscaling:index')


class AddRuleView(forms.ModalFormView):
    form_class = project_forms.AddRuleForm
    template_name = 'container/autoscaling/add_rule.html'
    modal_id = "add_rule_modal"
    modal_header = _("Add rule")
    submit_label = _("Add rule")	
    success_url = reverse_lazy('horizon:container:autoscaling:index')

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
