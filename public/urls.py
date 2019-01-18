from django.conf.urls import url

from public.views import *

urlpatterns = [

    # class based
    url(r'^$', HomeTemplateView.as_view(), name='home'),
    url(r'^workouts/$', WorkoutListView.as_view(), name='workouts'),
    url(r'^workout/(?P<pk>\d+)/$', WorkoutDetailView.as_view(), name='workout'),
    url(r'^workout-edit/(?P<pk>\d+)/$', WorkoutEditView.as_view(), name='edit_workout'),

    # api
    url(r'^api/workout-setup/$', setupWorkout, name='setup_workout'),
    url(r'^api/workout-update/(?P<pk>\d+)/$', updateWorkout, name='update_workout'),
]
