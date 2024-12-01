document.addEventListener('DOMContentLoaded', function () {
    const messageModal = document.getElementById('message-modal');
    const guardarModal = document.getElementById('guardar-modal');
    const guardarBtns = document.querySelectorAll('.register-btn');
    const closeGuardarModal = document.getElementById('close-guardar-modal');
    const confirmarGuardar = document.getElementById('confirmar-guardar');
    const cancelarGuardar = document.getElementById('cancelar-guardar');
    const verEnlaceDrive = document.querySelectorAll('.ver-drive');
    const verObservacion = document.querySelectorAll('.ver-observacion');
    const verResolucion = document.querySelectorAll('.ver-pdfResolucion');
    const verDictamen = document.querySelectorAll('.ver-pdfDictamen');
    const subirDictamen = document.querySelectorAll('.save-btn');

    verDictamen.forEach(function (verDictamen) {
        verDictamen.addEventListener('click', function () {
            const urlDrive = this.getAttribute('data-url');
            window.open(urlDrive, '_blank');
        })
    })

    verEnlaceDrive.forEach(function (verEnlaceDrive) {
        verEnlaceDrive.addEventListener('click', function () {
            const urlDrive = this.getAttribute('data-url');
            window.open(urlDrive, '_blank');
        })
    })

    verObservacion.forEach(function (verObservacion) {
        verObservacion.addEventListener('click', function () {
            const urlObs = this.getAttribute('data-url-obs');
            window.open(urlObs, '_blank');
        })
    })

    verResolucion.forEach(function (verResolucion) {
        verResolucion.addEventListener('click', function () {
            const urlDrive = this.getAttribute('data-url');
            window.open(urlDrive, '_blank');
        })
    })

    guardarBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            guardarModal.style.display = 'block';
            guardarModal.setAttribute('data-asignacion-id', btn.getAttribute('data-asignacion-id'));
        });
    });

    closeGuardarModal.addEventListener('click', function () {
        guardarModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === guardarModal) {
            guardarModal.style.display = 'none';
        }
    });

    subirDictamen.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const semestreAcademico = document.getElementById('semestre-academico').value;
            const dictamenPdf = document.getElementById('dictamen-pdf').files[0];

            if (!semestreAcademico || !dictamenPdf) {
                showMessageModal('No subió ningún archivo o no seleccionó ningún semestre.');
                return;
            }

            const formData = new FormData();
            formData.append('alumnoId', alumnoId);
            formData.append('semestreAcademico', semestreAcademico);
            formData.append('dictamenPdf', dictamenPdf);

            fetch(actualizarDictamen, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showMessageModal('Dictamen subido correctamente.');
                        document.getElementById('semestre-academico').value = '';
                        document.getElementById('dictamen-pdf').value = '';
                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showMessageModal('Error al subir el dictamen: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessageModal('Error en la solicitud. Intente de nuevo.');
                });
        });
    });

    confirmarGuardar.addEventListener('click', function () {
        const inputValue = document.getElementById('input-confirmar').value;
        const asignacionId = guardarModal.getAttribute('data-asignacion-id');

        if (inputValue === '') {
            showMessageModal('Debe llenar el campo');
            return;
        }

        fetch(actualizarAsignacion, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                asignacionId: asignacionId,
                enlace: inputValue
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    showMessageModal('Enlace actualizado correctamente.');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                } else {
                    showMessageModal('Error al actualizar: ' + data.message);
                }
                guardarModal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                showMessageModal('Error en la solicitud. Intente de nuevo.');
            });
    });

    cancelarGuardar.addEventListener('click', function () {
        guardarModal.style.display = 'none';
    });

    function showMessageModal(message) {
        const messageBody = document.getElementById('message-body');
        messageBody.innerText = message;
        messageModal.style.display = 'block';

        setTimeout(function () {
            messageModal.style.display = 'none';
        }, 1500);
    }
});
