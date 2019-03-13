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