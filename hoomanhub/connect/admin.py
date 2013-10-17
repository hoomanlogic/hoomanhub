from django.contrib import admin
from .models import Hooman, FlowRating, Story, Comment

admin.site.register(Hooman)
admin.site.register(FlowRating)
admin.site.register(Story)
admin.site.register(Comment)