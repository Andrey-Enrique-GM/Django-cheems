function toggleForm() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  loginForm.classList.toggle('hidden');
  registerForm.classList.toggle('hidden');
}



/* JAVASCRIPT PARA EL MODAL DE CREAR WORK ORDER */

document.addEventListener('DOMContentLoaded', () => {
    const openModalBtn = document.getElementById('openModalBtn');
    const changeStatusBtn = document.getElementById('changeStatusBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const modal = document.getElementById('createWorkOrderModal');
    const modalTitle = document.getElementById('modalTitle');
    const workOrderForm = document.getElementById('workOrderForm');
    const saveBtn = document.getElementById('saveBtn');

    const titleInput = document.getElementById('title');
    const descInput = document.getElementById('description');
    const statusSelect = document.getElementById('status');
    const titleFieldGroup = document.getElementById('titleFieldGroup');
    const descriptionFieldGroup = document.getElementById('descriptionFieldGroup');
    const statusFieldGroup = document.getElementById('statusFieldGroup');
    const createStatusNote = document.getElementById('createStatusNote');

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

            if (openModalBtn) {
                openModalBtn.textContent = 'Editar Orden';
                openModalBtn.style.backgroundColor = '#d97706';
            }
            if (changeStatusBtn) changeStatusBtn.disabled = false;
        });
    });

    const openModal = (mode) => {
        if (!modal || !workOrderForm) return;

        titleFieldGroup.classList.remove('hidden');
        descriptionFieldGroup.classList.remove('hidden');
        statusFieldGroup.classList.remove('hidden');
        createStatusNote.classList.add('hidden');
        titleInput.disabled = false;
        descInput.disabled = false;
        statusSelect.disabled = false;

        if (mode === 'create') {
            modalTitle.textContent = 'Crear Orden de Trabajo';
            saveBtn.textContent = 'Crear Orden';
            titleInput.value = '';
            descInput.value = '';
            statusFieldGroup.classList.add('hidden');
            statusSelect.disabled = true;
            createStatusNote.classList.remove('hidden');
            workOrderForm.action = '/create-work-order/';
        } else if (mode === 'edit' && selectedOrderData) {
            modalTitle.textContent = 'Editar Orden de Trabajo';
            saveBtn.textContent = 'Guardar Orden';
            titleInput.value = selectedOrderData.title;
            descInput.value = selectedOrderData.description;
            statusSelect.value = selectedOrderData.status;
            workOrderForm.action = `/update-work-order/${selectedOrderData.id}/`;
        } else if (mode === 'status' && selectedOrderData) {
            modalTitle.textContent = 'Modificar Estado de la Orden';
            saveBtn.textContent = 'Actualizar Estado';
            titleFieldGroup.classList.add('hidden');
            descriptionFieldGroup.classList.add('hidden');
            titleInput.disabled = true;
            descInput.disabled = true;
            statusSelect.value = selectedOrderData.status;
            workOrderForm.action = `/update-work-order-status/${selectedOrderData.id}/`;
        } else {
            return;
        }

        modal.classList.remove('hidden');
    };

    if (openModalBtn) {
        openModalBtn.addEventListener('click', () => {
            openModal(selectedOrderData ? 'edit' : 'create');
        });
    }
    if (changeStatusBtn) {
        changeStatusBtn.addEventListener('click', () => openModal('status'));
    }

    if (modal) {
        // Cerrar el modal
        const closeModal = () => modal.classList.add('hidden');

        if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
        if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);

        // Cerrar si se hace clic en el fondo oscuro fuera de la caja
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
});
