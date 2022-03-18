from django.db import models


class ActivePlanManager(models.Manager):
    def get_queryset(self):
        return super(ActivePlanManager, self).get_queryset().filter(active=True)