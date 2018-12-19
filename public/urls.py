from django.conf.urls import url

from public.views import *

urlpatterns = [
    # class based
    url(r'^$', HomeTemplateView.as_view(), name='home'),
    # api
    url(r'^api/workout-setup/$', setupWorkout, name='setup_workout'),
]
