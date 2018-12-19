# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from public.models import * 


# Class based views
class HomeTemplateView(TemplateView):
    template_name = 'public/home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(parent=None)
        return context


# API
def setupWorkout(request):
    # here, create workout, and all the WorkoutWithGroup necessary
    print request.POST, request.POST.get('groups')
    return JsonResponse({'status' : 'success'})

