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
from django.http import HttpResponse

from .models import Action, Flow, Phase, Tag
from .forms import ActionForm, FlowForm, PhaseForm


def get_tag_list(request):
    from json import dumps
    response = []
    if request.REQUEST.has_key('q'):
        for tag in Tag.objects.filter(name__icontains=request.REQUEST['q']):
            item = {'value': tag.name, 'name': tag.name}
            response.append(item)
    else:
        for tag in Tag.objects.all():
            item = {'value': tag.name, 'name': tag.name}
            response.append(item)

    return HttpResponse(dumps(response),
                        content_type='application/json; charset=UTF-8')


class MessageMixin(object):

    def tell_user(self, msg):
        messages.info(self.request, msg)


class HomeView(TemplateView):
    template_name = "plan/home.html"


class ActionCreateView(CreateView):
    model = Action
    success_url = reverse_lazy('plan:action_list')
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

    
class FlowCreateView(CreateView):
    model = Flow
    success_url = reverse_lazy('plan:flow_list')
    form_class = FlowForm
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


class FlowUpdateView(UpdateView):
    model = Flow


class FlowDeleteView(DeleteView):
    model = Flow
    success_url = reverse_lazy('flow-list')


class FlowDetailView(DetailView):
    model = Flow


class FlowListView(MessageMixin, ListView):
    model = Flow

    def get_queryset(self):
        # fetch parent queryset
        queryset = super(FlowListView, self).get_queryset()
        # get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            self.tell_user("Filtered to flows containing '{}'".format(q))
            # return a filtered queryset
            return queryset.filter(name__icontains=q)
        # return the base queryset
        return queryset


class FlowSearchView(TemplateView):
    template_name = "plan/_flow_search.html"
    

class PhaseCreateView(CreateView):
    model = Phase
    success_url = reverse_lazy('plan:phase_list')
    form_class = PhaseForm
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


class PhaseUpdateView(UpdateView):
    model = Phase


class PhaseDeleteView(DeleteView):
    model = Phase
    success_url = reverse_lazy('phase-list')


class PhaseDetailView(DetailView):
    model = Phase


class PhaseListView(MessageMixin, ListView):
    model = Phase

    def get_queryset(self):
        # fetch parent queryset
        queryset = super(PhaseListView, self).get_queryset()
        # get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            self.tell_user("Filtered to phases containing '{}'".format(q))
            # return a filtered queryset
            return queryset.filter(name__icontains=q)
        # return the base queryset
        return queryset


class PhaseSearchView(TemplateView):
    template_name = "plan/_phase_search.html"