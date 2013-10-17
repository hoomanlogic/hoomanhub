from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core import exceptions
from django.core.exceptions import ImproperlyConfigured
from django.forms import Form
from braces.views import LoginRequiredMixin
from .models import Action
from .forms import ActionForm


class MessageMixin(object):

    def tell_user(self, msg):
        messages.info(self.request, msg)


class HomeView(TemplateView):
    template_name = "plan/home.html"


class ActionCreateView(CreateView):
    model = Action
    success_url = reverse_lazy('plan:list')
    form_class = ActionForm
    #
    #def post(self, request, *args, **kwargs):
    #    self.object = None
    #    form_class = self.get_form_class()
    #    form = self.get_form(form_class)
    #    if form.is_valid():
    #        self.ensure_permissions(request.user, form.instance)
    #        return self.form_valid(form)
    #    else:
    #        return self.form_invalid(form)


class ActionUpdateView(UpdateView):
    model = Action


class ActionDeleteView(DeleteView):
    model = Action
    success_url = reverse_lazy('action-list')


class ActionDetailView(DetailView):
    model = Action


class ActionListView(MessageMixin, ListView):
    model = Action

    def get_queryset(self):
        # fetch parent queryset
        queryset = super(ActionListView, self).get_queryset()
        # get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            self.tell_user("Filtered to actions containing '{}'".format(q))
            # return a filtered queryset
            return queryset.filter(name__icontains=q)
        # return the base queryset
        return queryset


class ActionSearchView(TemplateView):
    template_name = "plan/_action_search.html"