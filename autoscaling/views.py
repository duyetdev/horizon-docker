from horizon import views
from openstack_dashboard.dashboards.docker.autoscaling import forms as project_forms
from openstack_dashboard.dashboards.docker.autoscaling import tables as project_tables
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
        context['vm_list'] = []
        if instances:
            for instance in instances:
                context['vm_list'].append({'id': instance.key_name, 'name': instance.name})

        # context['vm_list'] = ( 'vm-olp1', 'vm-olp2', 'vm-olp3' )
        context['current_vm'] = self.request.GET.get('vm', None)
        if not context['current_vm']:
            context['current_vm'] = context['vm_list'][0] \
                if len(context['vm_list']) > 0 else False


        return context

class AddRuleView(forms.ModalFormView):
    form_class = project_forms.AddRuleForm
    template_name = 'container/autoscaling/add_rule.html'
    modal_id = "add_rule_modal"
    modal_header = _("Add rule")
    submit_label = _("Add rule")    
    success_url = reverse_lazy('horizon:container:autoscaling:index')
    submit_url = reverse_lazy("horizon:container:autoscaling:add_rule")

class DeleteRuleView(forms.ModalFormView):
    pass