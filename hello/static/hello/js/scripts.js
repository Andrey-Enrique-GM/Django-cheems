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
    const modalTitle = document.getElementById('modalTitle');
    const workOrderForm = document.getElementById('workOrderForm');
    
    const titleInput = document.getElementById('title');
    const descInput = document.getElementById('description');
    const statusSelect = document.getElementById('status');

    let selectedOrderData = null; // Almacenará la orden seleccionada

    // Manejar selección de filas en la tabla work_order
    const rows = document.querySelectorAll('.selectable-row');
    rows.forEach(row => {
        row.addEventListener('click', (e) => {
            // Si se hace clic en la celda o enlace de 'Historial', no activar la selección de edición
            if (e.target.closest('.no-select') || e.target.classList.contains('btn-history-link')) {
                return;
            }

            // Remover selección previa
            rows.forEach(r => r.style.backgroundColor = '');
            
            // Marcar la fila actual visualmente
            row.style.backgroundColor = '#e2e8f0';
            
            // Guardar datos de esta orden
            selectedOrderData = {
                id: row.dataset.id,
                title: row.dataset.title,
                description: row.dataset.description,
                status: row.dataset.status
            };

            // Cambiar el botón superior a Editar
            if (openModalBtn) {
                openModalBtn.textContent = 'Editar Orden';
                openModalBtn.style.backgroundColor = '#d97706';
            }
        });
    });

    if (openModalBtn && modal) {
        // Abrir el modal
        openModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            if (selectedOrderData) {
                // MODO EDICIÓN
                modalTitle.textContent = 'Editar Orden de Trabajo';
                titleInput.value = selectedOrderData.title;
                descInput.value = selectedOrderData.description;
                statusSelect.value = selectedOrderData.status;
                
                workOrderForm.action = `/update-work-order/${selectedOrderData.id}/`;
            } else {
                // MODO CREACIÓN
                modalTitle.textContent = 'Crear Orden de Trabajo';
                titleInput.value = '';
                descInput.value = '';
                statusSelect.value = '1';
                workOrderForm.action = '/create-work-order/';
            }
            
            modal.classList.remove('hidden');
        });

        // Cerrar el modal
        const closeModal = () => modal.classList.add('hidden');

        if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
        if (cancelModalBtn) closeModalBtn.addEventListener('click', closeModal);

        // Cerrar si se hace clic en el fondo oscuro fuera de la caja
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
});
