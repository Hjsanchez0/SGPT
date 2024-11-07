document.addEventListener('DOMContentLoaded', function () {
    const messageModal = document.getElementById('message-modal');
    const semestreSelect = document.getElementById('semestre-select');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');
    const confirmModal = document.getElementById('confirm-modal');
    const confirmSend = document.getElementById('confirm-send');
    const cancelSend = document.getElementById('cancel-send');
    const agregarJuradoModal = document.getElementById('agregar-jurado-modal');
    const closeAgregarJuradoModal = document.getElementById('close-agregar-jurado-modal');
    const confirmAgregarJurado = document.getElementById('confirm-agregar-jurado');
    const cancelAgregarJurado = document.getElementById('cancel-agregar-jurado');
    const agregarJuradoButtons = document.querySelectorAll('.agregar-jurado');
    const eliminarJuradoButtons = document.querySelectorAll('.eliminar-jurado');
    const eliminarJuradoModal = document.getElementById('eliminar-jurado-modal');
    const confirmEliminarJurado = document.getElementById('confirm-eliminar-jurado');
    const cancelEliminarJurado = document.getElementById('cancel-eliminar-jurado');

    agregarJuradoButtons.forEach(button => {
        button.addEventListener('click', function() {
            agregarJuradoModal.style.display = 'block';
            agregarJuradoModal.setAttribute('data-proyecto-id', button.getAttribute('data-proyecto-id'));
        });
    });

    eliminarJuradoButtons.forEach(button => {
        button.addEventListener('click', function () {
            eliminarJuradoModal.style.display = 'block';
            eliminarJuradoModal.setAttribute('data-proyecto-id', button.getAttribute('data-proyecto-id'));
        });
    });

    closeAgregarJuradoModal.addEventListener('click', function() {
        agregarJuradoModal.style.display = 'none';
    });

    cancelAgregarJurado.addEventListener('click', function() {
        agregarJuradoModal.style.display = 'none';
    });

    cancelEliminarJurado.addEventListener('click', function () {
        eliminarJuradoModal.style.display = 'none';
    });

    confirmAgregarJurado.addEventListener('click', function() {
        const presidenteId = document.getElementById('presidente-select').value;
        const vocalId = document.getElementById('vocal-select').value;
        const secretarioId = document.getElementById('secretario-select').value;
        const proyectoId = agregarJuradoModal.getAttribute('data-proyecto-id'); 

        if (presidenteId === '' || vocalId === '' || secretarioId === '') {
            showMessageModal('Todos los roles deben ser seleccionados antes de asignar.');
            return; 
        }

        confirmModal.style.display = 'block';
    
        confirmSend.onclick = function() {
            fetch(actualizarJurado, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    presidenteId: presidenteId,
                    vocalId: vocalId,
                    secretarioId: secretarioId,
                    proyectoId: proyectoId,
                    administrativoId: administrativoId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessageModal('Jurados asignados correctamente.');
                    document.getElementById('presidente-select').value = '';
                    document.getElementById('vocal-select').value = '';
                    document.getElementById('secretario-select').value = '';
                    
                    setTimeout(function() {
                        location.reload();
                    }, 1500);
                } else {
                    showMessageModal('Error al asignar jurados: ' + data.error);
                }
                agregarJuradoModal.style.display = 'none';
                confirmModal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                showMessageModal('Error en la solicitud. Intente de nuevo.');
            });
        };
    
        cancelSend.onclick = function() {
            confirmModal.style.display = 'none';
        };
    });

    confirmEliminarJurado.addEventListener('click', function () {
        const proyectoId = eliminarJuradoModal.getAttribute('data-proyecto-id');

        fetch(eliminarJurado, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                proyectoId: proyectoId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessageModal('Jurados y fecha eliminados correctamente.');
                setTimeout(function () {
                    location.reload();
                }, 1500);
            } else {
                showMessageModal('Error al eliminar: ' + data.error);
            }
            eliminarJuradoModal.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            showMessageModal('Error en la solicitud. Intente de nuevo.');
        });
    });

    semestreSelect.addEventListener('change', function() {
        const semestreId = this.value;
        const semestreNombre = semestreSelect.options[semestreSelect.selectedIndex].text;

        Array.from(resultadosBusqueda.rows).forEach(row => {
            const semestreCells = row.cells[2];
            if (semestreCells) {
                const semestres = semestreCells.innerText.split(', ');
                const match = semestres.some(semestre => semestre.trim() === semestreNombre);
                row.style.display = match || row.rowIndex === 0 ? '' : 'none';
            }
        });
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
