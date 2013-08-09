# coding=utf-8
from django.http import HttpResponse
from mezzanine.forms.forms import FormForForm
from mezzanine.pages.models import Page
from mezzanine.utils.views import render

__author__ = 'pahaz'

from mezzanine.pages.page_processors import processor_for
from django.forms.util import ErrorList


@processor_for('interview')
def form_processor(request, page):
    """
    Display a built form and handle submission.
    """
    if request.method == 'POST':
        form = FormForForm(page.form,
                           request.POST or None,
                           request.FILES or None)
        if form.is_valid() and request.regstage:
            request.regstage.anketa = True
            request.regstage.save()

    return {'anketa': True, 'stage': True}


@processor_for('reverse')
def form_processor(request, page):
    """
    Display a built form and handle submission.
    """
    if request.method == 'POST':
        form = FormForForm(page.form,
                           request.POST or None,
                           request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['field_6'] == 'awqsAGkWSMguGwMG':
                if request.regstage:
                    request.regstage.task_1 = True
                    request.regstage.save()
            else:
                errors = form._errors.setdefault("field_6", ErrorList())
                errors.append(u'wrong key!')
                return render(request, 'pages/form.html', {'form': form})

    return {'stage': True}


@processor_for('network')
def form_processor(request, page):
    """
    Display a built form and handle submission.
    """
    if request.method == 'POST':
        form = FormForForm(page.form,
                           request.POST or None,
                           request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['field_5'] == 'Are_you_attentive?':
                if request.regstage:
                    request.regstage.task_2 = True
                    request.regstage.save()
            else:
                errors = form._errors.setdefault("field_5", ErrorList())
                errors.append(u'wrong key!')
                return render(request, 'pages/form.html', {'form': form})

    return {'stage': True}
