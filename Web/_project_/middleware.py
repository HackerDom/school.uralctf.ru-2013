# coding=utf-8
from django.utils.functional import SimpleLazyObject
from _project_.models import StageUser

__author__ = 'pahaz'


def get_stage(request):
    if not hasattr(request, '_cached_stage'):
        stage = None
        if request.user.is_authenticated():
            (stage,
             created) = StageUser.objects.get_or_create(user=request.user)

        request._cached_stage = stage
    return request._cached_stage


class StageUserMiddleware(object):
    def process_request(self, request):
        request.regstage = SimpleLazyObject(lambda: get_stage(request))
