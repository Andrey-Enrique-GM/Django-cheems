function toggleForm() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  loginForm.classList.toggle('hidden');
  registerForm.classList.toggle('hidden');
}