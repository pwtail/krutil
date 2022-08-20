from django.db.models import Field
from django.db.models.manager import BaseManager, ManagerDescriptor
from django.db import models, router
from django.db.models.signals import class_prepared
from django.db.models.utils import resolve_callables

from vinyl.meta import make_vinyl_model
from vinyl.model import ModelPlus
from vinyl.queryset import VinylQuerySet


class _VinylManager(BaseManager.from_queryset(VinylQuerySet)):
    """
    VinylManager itself.
    """
    model = None


class VinylManagerDescriptor(ManagerDescriptor):
    manager = None

    def __init__(self, model=None):
        self.manager = _VinylManager()
        if model:
            self.manager.model = model

    def __get__(self, instance, owner):
        assert not instance
        assert self.manager
        return self.manager

    def create_model(self, django_model, *args, **kw):
        self.manager.model = make_vinyl_model(django_model)

    #TODO: do not store pure django model?

    def __set_name__(self, owner, name):
        assert issubclass(owner, models.Model)
        self.manager.name = name
        self.django_model = owner
        create_model = lambda *args, **kw: self.create_model(owner, *args, **kw)
        class_prepared.connect(create_model, sender=owner)


VinylManager = VinylManagerDescriptor

