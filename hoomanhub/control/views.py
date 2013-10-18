from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView

from .models import Hooman
from .forms import HoomanForm


class HomeView(DetailView):
    template_name = "control/home.html"
    model = Hooman
    success_url = reverse_lazy('settings:home')
    form_class = HoomanForm
