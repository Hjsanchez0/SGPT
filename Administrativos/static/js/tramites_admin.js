document.addEventListener('DOMContentLoaded', function () {
    const messageModal = document.getElementById('message-modal');
    const observationModal = document.getElementById('observation-modal');
    const confirmObservation = document.getElementById('confirm-observation');
    const cancelObservation = document.getElementById('cancel-observation');
    const closeObservationModal = document.getElementById('close-observation-modal');
    const observarButtons = document.querySelectorAll('.observar-btn');
    const selectAllCheckbox = document.getElementById('select-all');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    const verPdfBtn = document.querySelectorAll('.ver-pdf');
    const verPdfCartaBtn = document.querySelectorAll('.ver-pdfCarta');
    const semestreSelect = document.getElementById('semestre-select');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');
    const enviarRespuestaBtn = document.querySelector('.register-btn');
    const confirmModal = document.getElementById('confirm-modal');
    const confirmSend = document.getElementById('confirm-send');
    const cancelSend = document.getElementById('cancel-send');
    const dniInput = document.getElementById('buscar-dni'); 
    const buscarBtn = document.getElementById('buscar-btn');

    observarButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartaId = this.getAttribute('data-carta-id');
            observationModal.dataset.cartaId = cartaId;
            observationModal.style.display = 'block';
        });
    });

    closeObservationModal.addEventListener('click', function() {
        observationModal.style.display = 'none';
    });

    cancelObservation.addEventListener('click', function() {
        observationModal.style.display = 'none';
    });

    buscarBtn.addEventListener('click', function() {
        const dniIngresado = dniInput.value.trim(); 
        
        Array.from(resultadosBusqueda.rows).forEach(row => {
            const dniCell = row.cells[1]; 
            if (dniCell) {
                const dniTexto = dniCell.innerText.trim();
                const dniList = dniTexto.split(',');
                const match = dniList.some(dni => dni.trim() === dniIngresado);
                row.style.display = match || row.rowIndex === 0 ? '' : 'none'; 
            }
        });
    });
    
    semestreSelect.addEventListener('change', function() {
        const semestreId = this.value;
        const semestreNombre = semestreSelect.options[semestreSelect.selectedIndex].text; 

        Array.from(resultadosBusqueda.rows).forEach(row => {
            const semestreCells = row.cells[5]; 
            if (semestreCells) {
                const semestres = semestreCells.innerText.split(', '); 
                const match = semestres.some(semestre => semestre.trim() === semestreNombre); 
                row.style.display = match || row.rowIndex === 0 ? '' : 'none'; 
            }
        });
    });

    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    verPdfBtn.forEach(function(verPdfBtn) {
        verPdfBtn.addEventListener('click', function() {
            const pdfUrl = this.getAttribute('data-url'); 
            window.open(pdfUrl, '_blank');
        });
    });

    verPdfCartaBtn.forEach(function(verPdfCartaBtn) {
        verPdfCartaBtn.addEventListener('click', function() {
            const pdfUrlCarta = this.getAttribute('data-url'); 
            window.open(pdfUrlCarta, '_blank');
        });
    });

    confirmObservation.addEventListener('click', function() {
        const observationText = document.getElementById('observation-textarea').value;
        const cartaId = observationModal.dataset.cartaId;

        if(observationText === ''){
            showMessageModal('Complete el campo de observación');
            return; 
        }
    
        fetch(observarCarta, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ carta_id: cartaId, observacion: observationText })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error en la actualización');
        })
        .then(data => {
            showMessageModal(data.message);
            observationModal.style.display = 'none';
            document.getElementById('observation-textarea').value = '';
            location.reload()
        })
        .catch(error => {
            console.error('Error:', error);
            showMessageModal('Error al actualizar la observación');
        });
    });

    enviarRespuestaBtn.addEventListener('click', function() {
        const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
        const selectedIds = [];

        selectedCheckboxes.forEach(checkbox => {
            selectedIds.push(checkbox.getAttribute('data-carta-id'));
        });

        if (selectedIds.length > 0) {
            confirmModal.style.display = 'block';

            confirmSend.onclick = function() {
                fetch(enviarRespuestaCarta, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ carta_ids: selectedIds })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        showMessageModal(data.message);
                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showMessageModal('Error al enviar la respuesta');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessageModal('Error al enviar la respuesta');
                });

                confirmModal.style.display = 'none';
            };

            cancelSend.onclick = function() {
                confirmModal.style.display = 'none';
            };
        } else {
            showMessageModal('Seleccione al menos un registro.');
        }
    });

    function showMessageModal(message) {
        const messageBody = document.getElementById('message-body');
        messageBody.innerText = message;
        messageModal.style.display = 'block';

        setTimeout(function() {
            messageModal.style.display = 'none';
        }, 1500);
    }
});