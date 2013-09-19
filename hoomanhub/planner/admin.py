from django.contrib import admin
from .models import Action, Decision, Flow, FlowIndex, Tag, Target, Execution, Phase, Cycle

admin.site.register(Action)
admin.site.register(Decision)
admin.site.register(Flow)
admin.site.register(FlowIndex)
admin.site.register(Tag)
admin.site.register(Target)
admin.site.register(Execution)
admin.site.register(Phase)
admin.site.register(Cycle)