from public.models import *

groups = [
    {
        'name': 'chest',
        'exercises': ['Bench press', 'Dumbbell press (incline)'],
    }, {
        'name': 'shoulders',
        'exercises': [],
    {
        'name': 'back',
        'exercises': [
            'Pull downs (wide grip)', 'Pull downs (close grip)', 'Rows (wide grip)', 
            'Rows (close grip)', 'Barbell rows', 'Face pulls', 'Wide grip pull ups',
            ''
        ],
    {
        'name': 'bicep',
        'exercises': [],
    {
        'name': 'tricep',
        'exercises': [],
    {
        'name': 'legs',
        'exercises': [],
    {
        'name': 'abs',
        'exercises': [],
    }
]

def initialize():
    for group in groups:
        new_group = Group.objects.get_or_create(name=group.name)
        for exercise in group.exercises:
            Exercise.objects.get_or_create(group=new_group, name=exercise)

