document.addEventListener('DOMContentLoaded', function() {
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


        for (let i = answers.length -1; i > 0; i--) {
        let rand = Math.floor(Math.random() * (i+1));
        let place = answers[i];
        answers[i] = answers[rand];
        answers[rand] = place;
        }

        answers.forEach(answer => {
            let button = document.createElement('button');
            button.className = 'btn btn-secondary answer-btn';
            button.textContent = decodeHtml(answer);
            button.onclick = function() {
                document.querySelectorAll('.answer-btn').forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
                selectedAnswer = answer;
                submitBtn.disabled = false;
            };
            answersDiv.appendChild(button);
        });

        buttonWidth();
    }

    submitBtn.addEventListener('click', function() {
        const correctAnswer = questions[currentQuestions].correct_answer;
        if(selectedAnswer === decodeHtml(correctAnswer)) {
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
                function sendData() { 
                    $.ajax({ 
                        url: '/updateScore', 
                        type: 'POST', 
                        contentType: 'application/json', 
                        data: JSON.stringify({ 'score': score }), 
                        success: function(response) { 
                            console.log("success"); 
                        }, 
                        error: function(error) { 
                            console.log(error); 
                        } 
                    }); 
                }
                sendData();
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