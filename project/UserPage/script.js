document.addEventListener('DOMContentLoaded', function() {
    const scoresList = document.getElementById('scoresList');

    function loadScores() {
        const scores = JSON.parse(localStorage.getItem('quizScores')) || [];
        scores.reverse();
        let userscoresHTML = scores.map((previous) => `<div class="previous-scores d-flex justify-content-between">
        <span class="score">Score: ${previous.score}</span>
        <span class="date">Date: ${previous.date}</span>
        </div>`).join('');

        scoresList.innerHTML = userscoresHTML;
    }

    loadScores();
});


const savedScores = JSON.parse(localStorage.getItem('quizScores')) || [];
savedScores.push(score);
localStorage.setItem('quizScores', JSON.stringify(savedScores));
