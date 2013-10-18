from django.db import models
from datetime import timedelta, datetime, date

from core.models import TimeStampedModel
from control.models import Hooman
from plan.models import Flow


#=======================================================================================================================
# Models
#=======================================================================================================================
class FlowRating(TimeStampedModel):
    hooman = models.ForeignKey(Hooman, related_name='flow_ratings')
    rating = models.FloatField()
    flow = models.ForeignKey(Flow, related_name='flow_ratings')


class Story(TimeStampedModel):
    hooman = models.ForeignKey(Hooman, related_name='stories')
    content = models.TextField()
    flow = models.ForeignKey(Flow, related_name='stories', blank=True, null=True)


class Comment(TimeStampedModel):
    hooman = models.ForeignKey(Hooman, related_name='comments')
    story = models.ForeignKey(Story, )
    parent = models.ForeignKey('self', blank=True, null=True)
    content = models.TextField()