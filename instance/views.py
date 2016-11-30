from horizon import views
from openstack_dashboard.dashboards.docker.instance import forms as project_forms
from openstack_dashboard.dashboards.docker.instance import tables as project_tables

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms

from horizon.utils import memoized

from openstack_dashboard import api


class IndexView(views.APIView):
    # A very simple class-based view...
    table_class = project_tables.InstancesTable
    template_name = 'docker/instance/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

class CreateContainerView(forms.ModalFormView):
    form_class = project_forms.CreateContainer
    template_name = 'docker/instance/create_container.html'
    modal_id = "create_container_modal"
    modal_header = _("Create Container")
    submit_label = _("Create Cotainer")	
