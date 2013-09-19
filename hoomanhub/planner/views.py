from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import Form
from braces.views import LoginRequiredMixin
from .models import Action


class ActionCreateView(CreateView):
    model = Action


class ActionUpdateView(UpdateView):
    model = Action


class ActionDeleteView(DeleteView):
    model = Action
    success_url = reverse_lazy('action-list')


class ActionDetailView(DetailView):
    model = Action


class ActionListView(ListView):
    model = Action

    def get_queryset(self):
        # fetch parent queryset
        queryset = super(ActionListView, self).get_queryset()
        # get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # return a filtered queryset
            return queryset.filter(name__icontains=q)
        # return the base queryset
        return queryset


class ActionSearchView(TemplateView):
    template_name = "planner/_action_search.html"