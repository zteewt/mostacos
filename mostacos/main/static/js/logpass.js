document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('login'); // Кнопка для открытия окна входа
    const loginPopup = document.getElementById('loginPopup');
    const registerPopup = document.getElementById('registerPopup');
    const showRegistration = document.getElementById('showRegistration'); // Ссылка для регистрации
    const loginUsernameInput = document.getElementById('username');
    const loginPasswordInput = document.getElementById('password');
    const loginMessage = document.getElementById('loginMessage');
    const registerButton = document.getElementById('registerButton');
    
    const overlay = document.getElementById('overlay');

    // Открытие всплывающего окна входа
    loginButton.addEventListener('click', (e) => {
        e.preventDefault();
        loginPopup.style.display = 'block';
        overlay.classList.add('active');
    });

    // Показать форму регистрации
    showRegistration.addEventListener('click', () => {
        loginPopup.style.display = 'none'; // Скрыть окно входа
        registerPopup.style.display = 'block'; // Показать окно регистрации
    });

    // Обработчик кнопки "Войти в аккаунт"
    document.getElementById('loginButton').addEventListener('click', () => {
        const username = loginUsernameInput.value;
        const password = loginPasswordInput.value;

        // Здесь вы можете добавить вашу логику проверки логина и пароля
        
        loginMessage.textContent = "Вы успешно зашли в аккаунт";
        loginMessage.style.display = 'block'; // Показать сообщение
    });

    // Обработчик кнопки "Зарегистрироваться"
    registerButton.addEventListener('click', () => {
        const registerUsername = document.getElementById('registerUsername').value;
        const registerPassword = document.getElementById('registerPassword').value;

        // Здесь вы можете добавить вашу логику регистрации

        alert("Вы успешно зарегистрированы!");
        registerPopup.style.display = 'none'; // Скрыть окно регистрации
        loginPopup.style.display = 'block'; // Показать окно входа
    });

    // Закрытие всплывающих окон при клике на подложку
    overlay.addEventListener('click', () => {
        loginPopup.style.display = 'none'; // Скрыть окно входа
        registerPopup.style.display = 'none'; // Скрыть окно регистрации
        overlay.classList.remove('active');
    });
});

