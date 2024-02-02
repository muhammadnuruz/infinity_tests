let token = '';
let currentTopicId = null;

document.getElementById('login').addEventListener('click', function() {
    const fullName = document.getElementById('fullName').value.trim();
    const password = document.getElementById('password').value.trim();

    // Ism va parolni tekshirish
    if (!fullName || !password) {
        alert('Ism va parolni kiriting!');
        return;
    }

    // Token olish uchun so'rov
    fetch('/api/auth/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ full_name: fullName, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Kirish ma\'lumotlari xato!');
        }
        return response.json();
    })
    .then(data => {
        token = data.access;
        document.getElementById('loginSection').classList.add('hide');
        document.getElementById('registerLink').style.display = 'none';
        loadTopics();
    })
    .catch((error) => {
        console.error('Xato:', error);
        alert('Xato: ' + error.message);
    });
});

function loadTopics() {
    // Mavzularni yuklash uchun so'rov
    fetch('/api/topics/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const buttonsContainer = document.getElementById('buttons');
        buttonsContainer.innerHTML = '';
        data.results.forEach(item => {
            const button = document.createElement('button');
            button.textContent = item.name;
            button.classList.add('btn');
            button.onclick = function() {
                currentTopicId = item.id;
                loadQuestionsForTopic(item.id);
                buttonsContainer.innerHTML = '';
            };
            buttonsContainer.appendChild(button);
        });
    });
}

// Qolgan funksiyalar

function loadQuestionsForTopic(topicId) {
    fetch(`/api/tests/get_test/${topicId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "You have completed all the tests for this topic.") {
            handleTestCompletion(data);
        } else {
            handleQuestionsAndAnswers(data);
        }
    })
    .catch(error => {
        console.error('Xato:', error);
        document.getElementById('submitResponse').innerHTML = 'Xato: ' + error;
    });
}

function handleQuestionsAndAnswers(data) {
    const qAndADiv = document.getElementById('questionsAndAnswers');
    qAndADiv.innerHTML = `<h3 class="question">${data.question_number + ': ' + data.question}</h3>`;

    data.answers.forEach((answer) => {
        const button = document.createElement('button');
        button.textContent = answer.answer;
        button.classList.add('btn', 'answer');
        button.onclick = function() {
            submitAnswer(answer.answer);
        };
        qAndADiv.appendChild(button);
    });
}

function submitAnswer(answer) {
    // Javobni yuborish uchun so'rov
    fetch('/api/tests/submit_answer/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer: answer })
    })
    .then(response => response.json())
    .then(submitData => {
        let responseDiv = document.getElementById('submitResponse');
        responseDiv.innerHTML = `<div class="response-message ${
            submitData.message === "Wrong answer!" ? 'wrong-answer' : 'correct-answer'
        }">${submitData.message}</div>`;

        if (submitData.message === "Test Yakunlandi!") {
            const qAndADiv = document.getElementById('questionsAndAnswers');
            qAndADiv.innerHTML = ''; // Barcha savol va javob tugmalarini o'chirish
        } else {
            loadQuestionsForTopic(currentTopicId); // Yana bir xil mavzu bo'yicha savollar yuklanadi
        }
    })
    .catch(error => {
        console.error('Xato:', error);
        document.getElementById('submitResponse').innerHTML = 'Xato: ' + error;
    });
}

function handleTestCompletion(data) {
    const qAndADiv = document.getElementById('questionsAndAnswers');
    const responseDiv = document.getElementById('submitResponse');

    // Javob xabarlarini tozalash
    responseDiv.innerHTML = '';

    let completionMessage = `
        <div class="test-completion-message">
            <h3>Test Yakunlandi!</h3>
            <ul>
                <li>Savollar soni: ${data.number_of_questions}</li>
                <li>To'g'ri javoblar: ${data.correct_questions}</li>
                <li>Noto'g'ri javoblar: ${data.wrong_questions}</li>
            </ul>
        </div>`;

    qAndADiv.innerHTML = completionMessage;
}

// Boshqa kodlar...

function showTestResults(data) {
    const resultsDiv = document.getElementById('testResults');
    const resultMessage = document.getElementById('resultMessage');
    const totalQuestions = document.getElementById('totalQuestions');
    const correctAnswers = document.getElementById('correctAnswers');
    const wrongAnswers = document.getElementById('wrongAnswers');

    // Ma'lumotlarni ko'rsatish
    resultMessage.textContent = data.message;
    totalQuestions.textContent = data.number_of_questions;
    correctAnswers.textContent = `To'g'ri javoblar: ${data.correct_questions}`;
    wrongAnswers.textContent = `Noto'g'ri javoblar: ${data.wrong_questions}`;

    // Natijalarni ko'rsatish uchun div-ni ko'rsatish
    resultsDiv.classList.remove('hide');

    // Yangi o'zgaruvchilarni yaratish
    const correctAnswersElement = document.createElement('li');
    correctAnswersElement.className = 'correct';
    correctAnswersElement.textContent = `To'g'ri javoblar: ${data.correct_questions}`;

    const wrongAnswersElement = document.createElement('li');
    wrongAnswersElement.className = 'wrong';
    wrongAnswersElement.textContent = `Noto'g'ri javoblar: ${data.wrong_questions}`;

    // Bitta mazmun qo'shib, qanday ma'lumotlarni ko'rsatishni tekshirib ko'ramiz
    resultsDiv.appendChild(correctAnswersElement);
    resultsDiv.appendChild(wrongAnswersElement);
}

// Boshqa kodlar...


const correctAnswersElement = document.createElement('li');
correctAnswersElement.className = 'correct';
correctAnswersElement.textContent = `To'g'ri javoblar: ${data.correct_questions}`;

const wrongAnswersElement = document.createElement('li');
wrongAnswersElement.className = 'wrong';
wrongAnswersElement.textContent = `Noto'g'ri javoblar: ${data.wrong_questions}`;
