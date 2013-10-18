from django.db import models
from datetime import timedelta, datetime, date


#=======================================================================================================================
# Abstracts
#=======================================================================================================================
class ArchiveableModel(models.Model):
    archived_on = models.DateField(blank=True, null=True)

    @property
    def is_archived(self):
        if self.archived_on is None:
            return False
        elif self.archived_on is not None and datetime.today().date() < self.archived_on:
            return False
        else:
            return True

    class Meta:
        abstract = True


class DocumentableModel(models.Model):
    NOTES_TYPE = ((0, 'plaintext'), (1, 'uri'), (2, 'html'), (3, 'rst'))
    docs = models.TextField(blank=True, null=True)
    docs_type = models.PositiveSmallIntegerField(choices=NOTES_TYPE, default=0)

    class Meta:
        abstract = True


class TaggableModel(models.Model):
    tags = models.ManyToManyField('Tag', blank=True, null=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """An abstract base class model that provides self-updating 'created' and 'modified' fields."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniquelyNamedModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True