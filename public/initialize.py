from public.models import *

# PPL:
# Chest // Shoulders
# Back // Arms
# Legs
# Abs when convenient

# exercises belonging to parent groups are compound lifts

groups = [
    {
        "title" : "Arms",
        "exercises" : [],
        "subgroups" : [
            {
                "title" : "Bicep",
                "exercises" : [
                    "Dumbbell hammer curls",
                    "Rope hammer curls",
                    "Traditional dumbbell curls",
                    "EZ bar curls",
                    "Plate hammer curls",
                    "Curl machine"
                ]
            }, {
                "title" : "Tricep",
                "exercises" : [
                    "Overhead rope extension",
                    "Rope extension",
                    "Dips",
                    "Dumbbell skullcrusher",
                    "Bar skullcrusher",
                    "V bar extension",
                    "Kick backs"
                ]
            }
        ]
    }, {
        "title" : "Back",
        "exercises" : [
            "Traditional deadlift",
            "Sumo deadlift"
        ],
        "subgroups" : [
            {
                "title" : "Vertical pull",
                "exercises" : [
                    "Lat pull down machine",
                    "Plate-loaded lat pull down",
                    "Wide grip pull ups",
                    "Reverse grip pull downs",
                    "Close grip pull downs",
                    "Cable pull overs",
                    "Dumbbell pull overs"
                ]
            }, {
                "title" : "Horizontal pull",
                "exercises" : [
                    "Row machine",
                    "Wide grip row",
                    "Barbell row",
                    "Dumbbell row"
                ]
            }
        ]
    }, {
        "title" : "Chest",
        "exercises" : ["Bench press"],
        "subgroups" : [
            {
                "title" : "Press",
                "exercises" : [
                    "Incline dumbbell press",
                    "Flat dumbbell press",
                    "Hammer strength machine",
                    "Grid bar press",
                    "Incline barbell press",
                    "Chest press machine"
                ]
            }, {
                "title" : "Flies",
                "exercises" : [
                    "Cable flies",
                    "Rising cable flies",
                    "Pec deck",
                    "Dumbbell flies",
                    "Incline dumbbell flies"
                ]
            }
        ]
    }, {
        "title" : "Legs",
        "exercises" : [
            "Squat",
            "Plate-loaded leg press",
            "Leg press machine"
        ],
        "subgroups" : [
            {
                "title" : "Quads",
                "exercises" : [
                    "Leg extension machine",
                    "Dumbbell lunges"
                ]
            }, {
                "title" : "Hamstring",
                "exercises" : [
                    "Hamstring curl machine",
                    "Dumbbell romanian deadlifts",
                    "Hanging hamstring curls"
                ]
            }, {
                "title" : "Calves",
                "exercises" : [
                    "Calf raise machine"
                ]
            }
        ]
    }, {
        "title" : "Shoulders",
        "exercises" : ["Standing overhead press"],
        "subgroups" : [
            {
                "title" : "Press",
                "exercises" : [
                    "Seated dumbbell press",
                    "Landmine overhead press",
                    "Arnies"
                ]
            }, {
                "title" : "Raises",
                "exercises" : [
                    "Dumbbell lateral raise",
                    "Lateral raise machine",
                    "Cable lateral raise"
                ]
            }, {
                "title" : "Rear delt",
                "exercises" : [
                    "Face pulls",
                    "Reverse flies"
                ]
            }
        ]
    }, {
        "title" : "Abs",
        "exercises" : [
            "Decline situps",
            "Twists",
            "Cable crunches"
        ]
    }
]


# not tested yet
def initialize():
    for group in groups:
        new_group, new_group_created = Group.objects.get_or_create(
            name=group['title']
        )
        for exercise in group.get('exercises', []):
            Exercise.objects.get_or_create(
                group=new_group,
                name=exercise
            )
        for subgroup in group.get('subgroups', []):
            new_subgroup, new_subgroup_created = Group.objects.get_or_create(
                name=subgroup['title'],
                parent=new_group
            )
            for sub_exercise in subgroup['exercises']:
                Exercise.objects.get_or_create(
                    group=new_subgroup,
                    name=sub_exercise
                )


for group in groups:
    indent_level = 0
    return_string = ''
    print(group['title'])
    indent_level += 1
    for exercise in group.get('exercises', []):
        print('  ' + exercise)
    indent_level += 1
    for subgroup in group.get('subgroups', []):
        print('    ' + subgroup['title'])
        for sub_exercise in subgroup['exercises']:
            print('      ' + sub_exercise)
