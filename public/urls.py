from django.conf.urls import url

from public.views import *

urlpatterns = [
    # class based
    url(r'^$', HomeTemplateView.as_view(), name='home'),
    url(r'^workout-create/$', WorkoutCreateView.as_view(), name='create_workout'),
    # api
    url(r'^api/workout-setup/$', setupWorkout, name='setup_workout'),
]
