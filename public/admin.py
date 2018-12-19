# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from public.models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Image)
admin.site.register(WorkoutWithGroup)
admin.site.register(WorkoutWithExercise)