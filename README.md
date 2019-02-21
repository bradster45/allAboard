allAboard - the gain train
=========

Hi, welcome to allAboard. A project I am building in my spare time to serve two main purposes:

1) To practice languages I use such as Python (Django), JS & jQuery, HTML & CSS.

2) To help me to track training progress with a slick, custom build workout generator.

### The application

On the homepage you're greeted by a simple form where using the select you can choose the groups you want to generate a workout for.

![Homepage](https://github.com/bradster45/allAboard/blob/master/public/static/public/images/screenshots/home.JPG)

When you've selected and saved, you head to the edit form where you can manually select exercises from the subgroups, or can use the random button to randomly select one exercise from each group.

![Generator](https://github.com/bradster45/allAboard/blob/master/public/static/public/images/screenshots/generator.JPG)

### The code

The main purpose of the application is the random generation of a workout using selected groups. I realised when in the gym I was doing the same exercises every time and was getting bored. See the jQuery snippet responsible, found in [workout_edit.html](https://github.com/bradster45/allAboard/blob/master/public/templates/public/workout_edit.html)

```JavaScript
// random clicked, randomly generate workout
$('#random').click(function(){
    // remove last randomized workout
    clearWorkout();
    // loop through groups
    $('#groups_pool .group .exercise-set').each(function(index, value){
        // get exercises and pick random
        var exercises = $(value).find('.exercise');
        var random = Math.floor(Math.random() * exercises.length);
        var exercise = exercises.eq(random);
        selectExercise(exercise);
    });
});
```

### Improvements to make

At some point I'd love to add models to potentially track sets, reps, weights. I'd also like to see analytics to see how many times I've done certain exercises per day trained. E.g. what percentage of my chest sessions have I done bench press?
