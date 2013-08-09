# coding=utf-8
from django.contrib.auth import get_user_model

__author__ = 'pahaz'

from django.db import models
from django.core.files.base import ContentFile
from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign
import datetime
import os
import requests

ULOGIN_FIELDS = ['first_name', 'last_name', 'sex', 'email']
ULOGIN_OPTIONAL = ['photo', 'photo_big', 'city', 'country', 'bdate']

User = get_user_model()

from jsonfield import JSONField


class UserInfo(models.Model):
    """
    Example model that stores extra information received from authentication
    provider
    """

    # Describes the response with code 'sex': 1 for female
    SEX_FEMALE = 1

    # and 2 for male
    SEX_MALE = 2

    def upload_photo(self, filename):
        return 'avatars/{}/{}/{}'.format(self.ulogin.network,
                                         self.ulogin.uid,
                                         os.path.basename(filename))

    def upload_photo_big(self, filename):
        return 'photos/{}/{}/{}'.format(self.ulogin.network,
                                        self.ulogin.uid,
                                        os.path.basename(filename))

    ulogin = models.ForeignKey(ULoginUser)
    sex = models.IntegerField(blank=True, null=True,
                              choices=(
                                  (SEX_MALE, 'male'),
                                  (SEX_FEMALE, 'female'),
                              ))
    user = models.ForeignKey(User,
                             verbose_name='user')
    photo = models.URLField(null=True, blank=True, )
    photo_big = models.URLField(null=True, blank=True, )
    city = models.CharField(blank=True, default='', max_length=255)
    country = models.CharField(blank=True, default='', max_length=255)
    bdate = models.DateField(verbose_name='Birthday', blank=True, null=True)
    json = JSONField()

    class Meta:
        unique_together = (('ulogin', 'user'),)


def catch_ulogin_signal(*args, **kwargs):
    user = kwargs['user']
    ulogin = kwargs['ulogin_user']
    json = kwargs['ulogin_data']

    user.first_name = json['first_name']
    user.last_name = json['last_name']
    user.email = json['email']
    user.save()

    data = {'ulogin': ulogin, 'user': user, 'json': json}

    for fld in ['sex', 'city', 'country', 'photo', 'photo_big']:
        if fld not in json:
            continue
        data[fld] = json[fld]

    if 'bdate' in json and json['bdate']:
        d, m, y = json['bdate'].split('.')
        data['bdate'] = datetime.datetime(int(y), int(m), int(d))

    userinfo, create = UserInfo.objects.get_or_create(**{'ulogin': ulogin,
                                                         'user': user})
    for x, y in data.iteritems():
        setattr(userinfo, x, y)
    userinfo.save()


assign.connect(receiver=catch_ulogin_signal,
               sender=ULoginUser)
