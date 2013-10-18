from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core import exceptions
from django.core.exceptions import ImproperlyConfigured
from django.forms import Form
from braces.views import LoginRequiredMixin
from django.http import HttpResponse

from .models import Action, Flow, Phase, Tag, Target
from .forms import ActionForm, ActionUpdateForm, FlowForm, PhaseForm


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

    #def post(self, request, *args, **kwargs):
    #    self.object = None
    #    form_class = self.get_form_class()
    #    form = self.get_form(form_class)
    #    if form.is_valid():
    #        self.ensure_permissions(request.user, form.instance)
    #        return self.form_valid(form)
    #    else:
    #        return self.form_invalid(form)


class ActionDeleteView(DeleteView):
    model = Action
    success_url = reverse_lazy('plan:action_list')

#todo: decide if methods for deletes would be better, if so, how do you return a status code? and enforce post?
#def delete_action(request, object_id, model):
#    from django.shortcuts import get_object_or_404
#    obj = get_object_or_404(model, id=object_id)
#    obj.delete()
#    request.user.message_set.create(message='The %s was deleted' % model._meta.verbose_name )
#	return HttpResponseRedirect("/")


class ActionUpdateView(UpdateView):
    model = Action
    template_name = "plan/action_detail.html"
    form_class = ActionUpdateForm
    success_url = reverse_lazy('plan:action_list')

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        if context['form'].cleaned_data['target'] and 'target' in context['form'].changed_data:
            target = Target()
            target.action = context['action']
            target.text = context['form'].cleaned_data['target']
            target.text_to_data()
            target.save()

        #return self.render_to_response(context)
        return super(ActionUpdateView, self).form_valid(form)


class ActionListView(MessageMixin, ListView):
    model = Action

    def __init__(self):
        self.query = ''

    def get_queryset(self):
        # datetime
        from datetime import date
        from django.db.models import Q
        # fetch parent queryset
        queryset = super(ActionListView, self).get_queryset()
        # get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            #self.tell_user("Filtered to actions containing '{}'".format(q))
            # return a filtered queryset
            return queryset.filter(Q(name__icontains=q) & (Q(archived_on__isnull=True) | Q(archived_on__gt=date.today())))
        else:
            return queryset.filter(Q(archived_on__isnull=True) | Q(archived_on__gt=date.today()))
        # return the base queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        q = self.request.GET.get("q")
        if q:
            context.update({
                'query': q
            })
        return context

class ActionSearchView(TemplateView):
    template_name = "plan/_action_search.html"

    
class FlowCreateView(CreateView):
    model = Flow
    success_url = reverse_lazy('plan:flow_list')
    form_class = FlowForm


class FlowUpdateView(UpdateView):
    model = Flow


class FlowDeleteView(DeleteView):
    model = Flow
    success_url = reverse_lazy('plan:flow-list')


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


class PhaseUpdateView(UpdateView):
    model = Phase


class PhaseDeleteView(DeleteView):
    model = Phase
    success_url = reverse_lazy('plan:phase-list')


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