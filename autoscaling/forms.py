from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api

class AddRuleForm(forms.SelfHandlingForm):
    metric_name = forms.ChoiceField(choices=[('CPU', _('CPU')), ('MEM', _('Mem'))],
            label=_("Metric"),
            required=True)

    upper_threshold = forms.IntegerField(max_value=100, min_value=50, label=_("Upper threshold"), required = True)
    lower_threshold = forms.IntegerField(max_value=50, min_value=0, label=_("Lower threshold"), required = True)
    node_up = forms.IntegerField(max_value=10, min_value=0, label=_("Node up"), required = True)
    node_down = forms.IntegerField(max_value=10, min_value=0, label=_("Node down"), required = True)
    
    def handle(self, request, data):
        try:
            # Create ceilometer event trigger 
            scaling_up = 'autoscaling_up_' + str(metric_name)
            scaling_down = 'autoscaling_down_' + str(metric_name)
            api.ceilometer.alarm_create(request, name=scaling_up, threshold=upper_threshold)
            api.ceilometer.alarm_create(request, name=scaling_down, threshold=lower_threshold)

            return True
        except Exception:
            # pass
            return True