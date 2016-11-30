from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api

from openstack_dashboard.dashboards.docker.instance import api
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