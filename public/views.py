# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from public.models import * 

# Class based views
class HomeTemplateView(TemplateView):
    template_name = 'public/home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

class WorkoutCreateView(CreateView):
	model = Workout

# API
def setupWorkout(request):
    # here, create workout, and all the WorkoutWithGroup necessary
    print request.POST
    return JsonResponse({'status' : 'success'})