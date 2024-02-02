let token = '';

const fullNameInput = document.getElementById('fullName');
const passwordInput = document.getElementById('password');
const loginSection = document.getElementById('loginSection');
const registerLink = document.getElementById('registerLink');
const buttonsContainer = document.getElementById('buttons');
const qAndADiv = document.getElementById('questionsAndAnswers');
const responseDiv = document.getElementById('submitResponse');
const errorModal = document.getElementById('errorModal');

function openModal(content) {
    const modalContent = document.getElementById('modalContent');
    modalContent.textContent = content;
    errorModal.style.display = 'block';
}

async function loginUser() {
    const fullName = fullNameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!fullName || !password) {
        openModal('Ism va parolni kiriting!');
        return;
    }

    try {
        const response = await fetch('/api/auth/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ full_name: fullName, password: password })
        });

        if (!response.ok) {
            throw new Error('Kirish ma\'lumotlari xato!');
        }

        const data = await response.json();
        token = data.access;
        loginSection.classList.add('hide');
        registerLink.style.display = 'none';
        await loadTopics();
    } catch (error) {
        console.error('Xato:', error);
        openModal('Xato: ' + error.message);
    }
}

function loadTopics() {
    fetch('/api/topics/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
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
        responseDiv.innerHTML = 'Xato: ' + error;
    });
}

function handleQuestionsAndAnswers(data) {
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
            qAndADiv.innerHTML = '';
        } else {
            loadQuestionsForTopic(currentTopicId);
        }
    })
    .catch(error => {
        console.error('Xato:', error);
        responseDiv.innerHTML = 'Xato: ' + error;
    });
}

function handleTestCompletion(data) {
    qAndADiv.innerHTML = '';

    responseDiv.innerHTML = `
        <div class="test-completion-message">
            <h3>Test Yakunlandi!</h3>
            <ul>
                <li>Savollar soni: ${data.number_of_questions}</li>
                <li>To'g'ri javoblar: ${data.correct_questions}</li>
                <li>Noto'g'ri javoblar: ${data.wrong_questions}</li>
            </ul>
        </div>`;
}

function showTestResults(data) {
    const resultsDiv = document.getElementById('testResults');
    const resultMessage = document.getElementById('resultMessage');
    const totalQuestions = document.getElementById('totalQuestions');
    const correctAnswers = document.getElementById('correctAnswers');
    const wrongAnswers = document.getElementById('wrongAnswers');

    resultMessage.textContent = data.message;
    totalQuestions.textContent = data.number_of_questions;
    correctAnswers.textContent = `To'g'ri javoblar: ${data.correct_questions}`;
    wrongAnswers.textContent = `Noto'g'ri javoblar: ${data.wrong_questions}`;

    resultsDiv.classList.remove('hide');
}

let correctAnswersElement = document.createElement('li');
correctAnswersElement.className = 'correct';
correctAnswersElement.textContent = `To'g'ri javoblar: ${data.correct_questions}`;

let wrongAnswersElement = document.createElement('li');
wrongAnswersElement.className = 'wrong';
wrongAnswersElement.textContent = `Noto'g'ri javoblar: ${data.wrong_questions}`;
