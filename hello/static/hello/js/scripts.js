function toggleForm() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  loginForm.classList.toggle('hidden');
  registerForm.classList.toggle('hidden');
}



/* JAVASCRIPT PARA EL MODAL DE CREAR WORK ORDER */

document.addEventListener('DOMContentLoaded', () => {
    const openModalBtn = document.getElementById('openModalBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const modal = document.getElementById('createWorkOrderModal');

    if (openModalBtn && modal) {
        // Abrir el modal al hacer clic en + Crear Orden
        openModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.remove('hidden');
        });

        // Función para cerrar el modal
        const closeModal = () => {
            modal.classList.add('hidden');
        };

        if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
        if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);

        // Cerrar si se hace clic en el fondo oscuro fuera de la caja
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });
    } else {
        console.warn('No se encontró el botón u ocultó el modal.');
    }
});