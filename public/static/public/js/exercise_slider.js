// hides exercises lists
function hideExercises() {
    $('.exercises').slideUp();
    $('.expanded').removeClass('expanded');
};

// shows selected exercises list
function showExercises(obj, exercises) {
    $(exercises).slideDown();
    $(obj).addClass('expanded');
};

// when group title is clicked
$('.group-title').click(function () {

    // find it's exercise list and show/hide it
    var exercises = $(this).closest('.exercise-set').find('.exercises');

    if ($(this).hasClass('expanded')) {

        hideExercises();
    } else {

        hideExercises();
        showExercises(this, exercises);
    };
});
