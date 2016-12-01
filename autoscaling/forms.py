from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api

from openstack_dashboard.dashboards.docker.autoscaling import api
docker_driver = api.DockerDriver()

class CreateContainer(forms.SelfHandlingForm):
    docker_image = forms.CharField(max_length=250, label=_("Docker Image"), required = True)
    docker_number = forms.IntegerField(max_value=20, label=_("Number of Instance"))

    def handle(self, request, data):
        try:
            print 'Create docker %s with %s instance' % (data['docker_image'], data['docker_number'])
            docker_driver.container_create(data['docker_image'])

            return True
        except Exception:
            exceptions.handle(request,
                              _('Unable to create container.'))

class AddRuleForm(forms.SelfHandlingForm):
    metric_name = forms.ChoiceField(choices=[('CPU', _('CPU')), ('MEM', _('Mem'))],
            label=_("Metric"),
            required=True)

    upper_threshold = forms.IntegerField(max_value=100, min_value=50, label=_("Upper threshold"), required = True)
    lower_threshold = forms.IntegerField(max_value=50, min_value=0, label=_("Lower threshold"), required = True)
    
    def handle(self, request, data):
        try:
            # print 'Create docker %s with %s instance' % (data['docker_image'], data['docker_number'])
            # docker_driver.container_create(data['docker_image'])

            return True
        except Exception:
            exceptions.handle(request, _('Unable to create new rule.'))