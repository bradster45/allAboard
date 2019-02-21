# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models


class TimeStampedModel(models.Model):
    """
    abstract model adding creation / last update fields
    """
    # simplify created into auto_now_add=True
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


# can see the structure of groups in initialize.py
class Group(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    # add parent, FK to self
    parent = models.ForeignKey('self', related_name='subgroups', blank=True, null=True)

    def __str__(self, ):
        return self.name


class Workout(TimeStampedModel):
    groups = models.ManyToManyField(
        'Group', through='WorkoutWithGroup',
        through_fields=('workout', 'group'),
        related_name='workouts'
    )
    exercises = models.ManyToManyField(
        'Exercise', through='WorkoutWithExercise',
        through_fields=('workout', 'exercise'),
        related_name='workouts')
    date = models.DateField(blank=True, null=True)

    def __str__(self, ):
        string = ''
        for index, group in enumerate(self.groups.all()):
            if index != 0:
                string += ' //'
            string += ' {}'.format(group.name)
        return string

    def construct_tree(self, ):
        groups = []
        for group in self.groups.all():
            group = {
                'name': group,
                # get all exercises related to this workout, and group (as well as child groups)
                'exercises': self.exercises.filter(
                    models.Q(group=group) | models.Q(group__parent=group)
                )
            }
            groups.append(group)
        return groups


class Exercise(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='exercises')
    description = models.TextField()

    def __str__(self, ):
        return '{} // {}'.format(self.group.name, self.name)


class Image(TimeStampedModel):
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='exercises/')


class WorkoutWithGroup(TimeStampedModel):
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='workouts_with_groups')
    workout = models.ForeignKey(
        'Workout', on_delete=models.CASCADE, related_name='workouts_with_groups')

    class Meta:
        unique_together = (
            ('group', 'workout', ),
        )


class WorkoutWithExercise(TimeStampedModel):
    exercise = models.ForeignKey(
        'Exercise', on_delete=models.CASCADE, related_name='workouts_with_exercises')
    workout = models.ForeignKey(
        'Workout', on_delete=models.CASCADE, related_name='workouts_with_exercises')
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (
            ('exercise', 'workout', ),
            ('workout', 'order', ),
        )

    def save(self, *args, **kwargs):
        # todo
        # order = last order + 1 by default
        if not self.order:
            wwe = WorkoutWithExercise.objects.filter(workout=self.workout).order_by('order')
            if wwe.exists():
                self.order = wwe.last().order + 1
            else:
                self.order = 0

        return super(WorkoutWithExercise, self).save(*args, **kwargs)
