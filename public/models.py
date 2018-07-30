# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.functional import lazy
from django.utils.timezone import localtime, now


def get_tz_aware_now():
    return localtime(now())


class TimeStampedModel(models.Model):
    """
    abstract model adding creation / last update fields
    """
    created = models.DateTimeField(
        default=lazy(get_tz_aware_now, datetime.datetime)()
    )
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = localtime(now())
        return super(TimeStampedModel, self).save(*args, **kwargs)

class Group(TimeStampedModel):
    name = models.CharField(max_length=255)

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


class Exercise(TimeStampedModel):
    name = models.CharField(max_length=255)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='exercises')
    description = models.TextField()


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

    class Meta:
        unique_together = (
            ('exercise', 'workout', ),
        )