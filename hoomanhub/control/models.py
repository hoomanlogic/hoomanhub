from django.db import models
from datetime import timedelta, datetime, date
from core.models import TimeStampedModel, UniquelyNamedModel

#=======================================================================================================================
# Models
#=======================================================================================================================
class Hooman(TimeStampedModel, UniquelyNamedModel):
    email = models.EmailField()