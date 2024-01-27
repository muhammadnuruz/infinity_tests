document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:8000/api/users/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',  // Qo'shimcha header
        },
        mode: 'cors',  // CORS-ni yoqish
        credentials: 'include',  // Credentiallarni o'zgartiring
        body: JSON.stringify({ full_name: fullName, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.password) {
            // Ro'yxatdan o'tish muvaffaqiyatli bo'lsa, bosh sahifaga yo'naltirish
            window.location.href = 'http://127.0.0.1:8000/';
        } else {
            // Xabar ko'rsatish
            document.getElementById('message').textContent = data.full_name;
        }
    })
    .catch(error => {
        console.error('Xato:', error);
        document.getElementById('message').textContent = 'Xato: ' + error;
    });
});
