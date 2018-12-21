# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from public.models import * 


# Class based views
class HomeTemplateView(TemplateView):
    template_name = 'public/home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(parent=None)
        return context


class WorkoutListView(ListView):
    template_name = 'public/workout_list.html'
    paginate_by = 20
    model = Workout


class WorkoutDetailView(DetailView):
    template_name = 'public/workout_detail.html'
    model = Workout
    def get_context_data(self, **kwargs):
        context = super(WorkoutDetailView, self).get_context_data(**kwargs)
        context['object'] = Group.objects.filter(parent=None)
        return context


class WorkoutEditView(DetailView):
    template_name = 'public/workout_edit.html'
    model = Workout
    def get_context_data(self, **kwargs):
        context = super(WorkoutEditView, self).get_context_data(**kwargs)
        context['object'] = Group.objects.filter(parent=None)
        return context


# API
def setupWorkout(request):
    # here, create workout, and all the WorkoutWithGroup necessary
    groups = request.POST.getlist('groups[]', [])
    messages = []
    if len(groups) > 0:
        # create workout and attach groups, return ID for redirect to edit form
        workout = Workout.objects.create()
        print(workout)
        for group in groups:
            WorkoutWithGroup.objects.create(group=Group.objects.get(id=group), workout=workout)
        if len(messages) == 0:
            return JsonResponse({
                'status' : 'success',
                'workout_id' : workout.id
            })
    else:
        messages.append('Provide some groups to create a workout.')
    return JsonResponse({
        'status' : 'failed',
        'messages' : messages
    })

