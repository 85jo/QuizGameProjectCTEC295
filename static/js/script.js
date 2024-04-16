document.addEventListener('DOMContentLoaded', function () {
    let questions = [];
    let currentQuestions = 0;
    let score = 0;
    let selectedAnswer = '';
    let submitBtn = document.getElementById('submitBtn');
    let scoreDisplay = document.getElementById('scoreBox');

    function decodeHtml(html) {
        let txt = document.createElement("textarea");
        txt.innerHTML = html;
        return txt.value;
    }


    function fetchQuestions() {
        fetch('https://opentdb.com/api.php?amount=5&type=multiple')
            .then(response => response.json())
            .then(data => {
                data.results.forEach(question => questions.push(question));
                displayQuestion();
            })
            .catch(error => console.error('Error grabbing questions:', error));
    }

    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array [j]] = [array[j], array[i]];
        }
    }

    function quizEndOptions() {
        const endOptions = document.createElement('div');
        endOptions.innerHTML = `<button onclick="window.location.href='/dashboard'" class="btn-primary btn">Profile</button>
        <button onclick="location.reload()" class="btn-primary btn">Take Quiz Again</button>
        <button onclick="window.location.href='/leaderboard'" class="btn-primary btn">Leaderboard</button>
        <button onclick="window.location.href='/logout'" class="btn-primary btn">Logout</button>`;
        document.getElementById('result').appendChild(endOptions);

    }


    function displayQuestion() {
        if (currentQuestions >= questions.length) {
            document.getElementById('question').textContent = "Quiz Complete!";
            document.getElementById('answers').innerHTML = '';
            submitBtn.style.display = 'none';
            return;
        }

        const question = questions[currentQuestions];
        document.getElementById('question').textContent = decodeHtml(question.question);
        const answersDiv = document.getElementById('answers');
        answersDiv.innerHTML = '';

        const answers = [question.correct_answer, ...question.incorrect_answers];

        shuffle(answers);

        
        answers.forEach(answer => {
            let button = document.createElement('button');
            button.className = 'btn btn-secondary answer-btn';
            button.textContent = decodeHtml(answer);
            button.onclick = function () {
                document.querySelectorAll('.answer-btn').forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
                selectedAnswer = answer;
                submitBtn.disabled = false;
            };
            answersDiv.appendChild(button);
        });

        buttonWidth();
    }

    submitBtn.addEventListener('click', function () {
        const correctAnswer = questions[currentQuestions].correct_answer;
        if (selectedAnswer === decodeHtml(correctAnswer)) {
            score += 5;
            document.getElementById('result').textContent = 'You got it!';
        } else {
            document.getElementById('result').textContent = 'Wrong! The answer is: ' + decodeHtml(correctAnswer);
        }

        scoreDisplay.textContent = 'Score: ' + score;
        submitBtn.disabled = true;
        currentQuestions++;

        setTimeout(() => {
            if (currentQuestions < questions.length) {
                displayQuestion();
            } else {
                scoreDisplay.textContent += ". Quiz complete!";
                const scores = JSON.parse(localStorage.getItem('quizScores')) || [];
                const quizdate = new Date().toLocaleString();

                scores.push({
                    score: score,
                    date: quizdate
                });
                localStorage.setItem('quizScores', JSON.stringify(scores));
                submitBtn.style.display = 'none';
                quizEndOptions();
            }
        }, 1500);
    });

    fetchQuestions();
});

function buttonWidth() {
    let maxWidth = 0;
    const answerButtons = document.querySelectorAll('.answer-btn');
    answerButtons.forEach(button => {
        const width = button.offsetWidth;
        if (width > maxWidth) {
            maxWidth = width;
        }
    });
    answerButtons.forEach(button => {
        button.style.width = maxWidth + 'px';
    });
}

document.addEventListener('DOMContentLoaded', function () {
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

