# coding=utf-8
from django.db import models
from mezzanine.accounts.models import User


class StageUser(models.Model):
    user = models.OneToOneField(User)

    task_1 = models.BooleanField(default=False)
    task_2 = models.BooleanField(default=False)

    anketa = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Вы заполнили анкету : {0}'.format(self.anketa)

    def all(self):
        return self.task_1 and self.task_2 and self.anketa