from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

from .models import Hooman
from .forms import HoomanForm


class HomeView(TemplateView):
    template_name = "control/home.html"
    model = Hooman
    success_url = reverse_lazy('control:home')
    form_class = HoomanForm
