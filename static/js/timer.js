document.addEventListener('DOMContentLoaded', function() {
    const timerDisplay = document.getElementById('global-timer');
    let timeLeft = 600; // 10 minutes in seconds
    let timerInterval;

    // Load timer state from localStorage
    const savedTimer = localStorage.getItem('quizTimer');
    if (savedTimer) {
        const savedTime = JSON.parse(savedTimer);
        const elapsed = Math.floor((Date.now() - savedTime.startTime) / 1000);
        timeLeft = Math.max(0, savedTime.timeLeft - elapsed);
        
        if (timeLeft > 0) {
            startTimer();
        } else {
            timerDisplay.textContent = '00:00';
            localStorage.removeItem('quizTimer');
        }
    }

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function startTimer() {
        // Save initial timer state
        localStorage.setItem('quizTimer', JSON.stringify({
            startTime: Date.now(),
            timeLeft: timeLeft
        }));

        updateTimerDisplay();
        
        timerInterval = setInterval(function() {
            timeLeft--;
            updateTimerDisplay();
            
            // Update localStorage
            localStorage.setItem('quizTimer', JSON.stringify({
                startTime: Date.now(),
                timeLeft: timeLeft
            }));

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                localStorage.removeItem('quizTimer');
                // Redirect to home page when time runs out
                window.location.href = '/';
            }
        }, 1000);
    }

    // Start timer when clicking the Start button on index page
    const startButton = document.getElementById('start-quiz');
    if (startButton) {
        startButton.addEventListener('click', function() {
            timeLeft = 600;
            startTimer();
        });
    }

    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            const savedTimer = localStorage.getItem('quizTimer');
            if (savedTimer) {
                const savedTime = JSON.parse(savedTimer);
                const elapsed = Math.floor((Date.now() - savedTime.startTime) / 1000);
                timeLeft = Math.max(0, savedTime.timeLeft - elapsed);
                updateTimerDisplay();
                
                if (timeLeft > 0) {
                    startTimer();
                } else {
                    clearInterval(timerInterval);
                    timerDisplay.textContent = '00:00';
                    localStorage.removeItem('quizTimer');
                }
            }
        }
    });
}); 