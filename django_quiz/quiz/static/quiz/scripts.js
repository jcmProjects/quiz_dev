document.getElementById("start_btn").addEventListener("click", function goFullscreen() {
    var elem = document.getElementById("myQuiz");
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } 
    else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
    } 
    else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
    } 
    else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
    }

    document.getElementById("btn_footer").style.visibility = "visible";
});

document.addEventListener("fullscreenchange", function(event) {
    if (document.fullscreenElement) {
        // Window is in fullscren. Do nothin.
    }
    else {
        document.getElementById("btn_footer").style.visibility = "hidden";
    }
});

function startTimer(duration, display) {
var start = Date.now(),
    diff,
    minutes,
    seconds;
function timer() {
    // get the number of seconds that have elapsed since 
    // startTimer() was called
    diff = duration - (((Date.now() - start) / 1000) | 0);

    if (diff <= 0) {
        diff = 0;
    }
    display.textContent = diff;
};
// we don't want to wait a full second before the timer starts
timer();
setInterval(timer, 1000);
}

document.getElementById("play_btn").addEventListener("click", function () {
var timeRemaining = {{ object.duration }},
    display = document.querySelector('#time');
startTimer(timeRemaining, display);
});
