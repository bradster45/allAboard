# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import datetime

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


class SearchMixin(object):
    query_words = []  # strings to filter by
    search_vector = []  # model fields to be filtered

    def get_context_data(self, **kwargs):
        """
        add the query and query_words to the context
        """
        context = super(SearchMixin, self).get_context_data(**kwargs)
        # if anything meaningfull was searched
        q = self.request.GET.get('q', False)
        if q:
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
        if len(self.query_words) > 0:
            context['q'] = q
            context['query_words'] = self.query_words
        return context


class IcontainsSearchMixin(SearchMixin):
    def get_queryset(self, ):
        qs = super(IcontainsSearchMixin, self).get_queryset()
        q = self.request.GET.get('q')
        if q is not None and q != '':
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
            if len(self.query_words) > 0:
                for vector in self.search_vector:
                    for word in self.query_words:
                        kwargs = {}
                        kwargs[vector + '__icontains'] = word
                        qs = qs.filter(**kwargs)
        return qs


class FullTextSearchMixin(SearchMixin):
    """
    This mixin will perform a full text search on this app's article lists.
    If postgres is not used it will do a slower icontains search
    on the relevant fields annotating a similar rank.
    """

    def get_queryset(self, ):
        # fetch the queryset from the parent class
        qs = super(FullTextSearchMixin, self).get_queryset()
        # get the search parameter if any
        q = self.request.GET.get('q')
        if q is not None and q != '':
            # split the terms by whitespace and discard any below 3 chars.
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
            if len(self.query_words) > 0:
                search_query = None
                for vector in self.search_vector:
                    for word in self.query_words:
                        if search_query is None:
                            search_query = models.Q(
                                **{vector + "__icontains": word})
                        else:
                            search_query = search_query & models.Q(
                                **{vector + "__icontains": word})
                return qs.filter(search_query).distinct()
        return qs


class WorkoutListView(IcontainsSearchMixin, ListView):
    template_name = 'public/workout_list.html'
    paginate_by = 20
    model = Workout
    ordering = '-date'
    search_vector = ['date']


class WorkoutDetailView(DetailView):
    template_name = 'public/workout_detail.html'
    model = Workout


class WorkoutEditView(DetailView):
    template_name = 'public/workout_edit.html'
    model = Workout
    def get_context_data(self, **kwargs):
        context = super(WorkoutEditView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(parent=None)
        return context


class GroupListView(ListView):
    model = Group
    queryset = Group.objects.filter(parent=None)


# API
def setupWorkout(request):
    # here, create workout, and all the WorkoutWithGroup necessary
    groups = request.POST.getlist('groups[]', [])
    messages = []
    if len(groups) > 0:
        # create workout and attach groups, return ID for redirect to edit form
        workout = Workout.objects.create(date=datetime.datetime.now())
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


def updateWorkout(request, pk):
    workout = Workout.objects.get(pk=pk)
    exercises = request.POST.getlist('exercises[]', [])
    messages = []
    if len(exercises) > 0:
        workout.workouts_with_exercises.all().delete()
        for exercise in exercises:
            WorkoutWithExercise.objects.create(
                exercise=Exercise.objects.get(id=exercise),
                workout=workout
            )
        date = request.POST.get('date', False)
        if date:
            workout.date = date
        workout.save()
        if len(messages) == 0:
            return JsonResponse({
                'status': 'success'
            })
    else:
        messages.append('Provide some groups to create a workout.')
    return JsonResponse({
        'status': 'failed',
        'messages': messages
    })
