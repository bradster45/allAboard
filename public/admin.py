# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from public.models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(Exercise)
admin.site.register(Image)


class WorkoutWithGroupInline(admin.TabularInline):
    extra = 0
    model = WorkoutWithGroup


class WorkoutWithExerciseInline(admin.TabularInline):
    extra = 0
    model = WorkoutWithExercise


class WorkoutAdmin(admin.ModelAdmin):
    inlines = [
        WorkoutWithGroupInline,
        WorkoutWithExerciseInline
    ]

admin.site.register(Workout, WorkoutAdmin)
