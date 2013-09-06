# Create your views here.
from .models import Action, Flow, Tag


def blah():
    a = Action()
    t = Tag()

    t.id = 'planname'
    t.save()

    a.id = 'blah'
    a.tags.add(t)

    a.save()