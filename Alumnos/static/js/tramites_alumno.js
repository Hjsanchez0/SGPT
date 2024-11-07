document.addEventListener('DOMContentLoaded', function (){
    const registrarTramite = document.getElementById('registrar-tramite');
    const seguimientoTramite = document.getElementById('seguimiento-tramite');
    const messageModal = document.getElementById('message-modal');
    const modal1 = document.getElementById('confirmation-modal1');
    const confirmUpdate = document.getElementById('confirm-update');
    const cancelUpdate = document.getElementById('cancel-update');
    const closeModal1 = document.getElementById('close-modal1');
    const tramiteSelect = document.getElementById('tramite-select');
    const opcionesAdicionales = document.getElementById('opciones-adicionales');
    const verPdfBtn = document.getElementById('ver-pdf');
    const registerBtn = document.querySelector('.register-btn');
    const verPdfCartaBtn = document.querySelectorAll('.ver-pdfCarta');
    
    tramiteSelect.selectedIndex = 0;
    opcionesAdicionales.style.display = 'none';

    let contenidoTemporal = '';
    const textarea = document.getElementById('objeto-textarea');

    window.addEventListener('load', function() {
        contenidoTemporal = textarea.value;
    });

    textarea.addEventListener('input', function() {
        contenidoTemporal = this.value; 
    });

    registerBtn.addEventListener('click', function () {
        modal1.style.display = 'block';
    });

    cancelUpdate.addEventListener('click', function () {
        modal1.style.display = 'none';
    });
        
    verPdfBtn.addEventListener('click', function() {
        const pdfUrl = this.getAttribute('data-url');
        const contenido = contenidoTemporal;
        const firmaInput = document.getElementById('firma');
        const firmaFile = firmaInput.files[0];
    
        const formData = new FormData();
        formData.append('contenido', contenido);
        if (firmaFile) {
            formData.append('firma', firmaFile);
        }
    
        fetch(pdfUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Error al generar el PDF');
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            window.open(url, '_blank');
        })
        .catch(error => {
            console.error(error);
            showMessageModal('No se pudo generar el PDF.');
        });
    });

    confirmUpdate.addEventListener('click', function(e) {
        e.preventDefault();  
        let formData = new FormData();
    
        const tramite = document.getElementById('tramite-select').value;
    
        formData.append('proyecto_id', idProyecto);
        formData.append('semestre_id', idSemestre);
        formData.append('tramite', tramite);
    
        const contenido = contenidoTemporal
        const firmaInput = document.getElementById('firma');
        const firmaFile = firmaInput.files[0];
    
        formData.append('contenido', contenido);
        if (firmaFile) {
            formData.append('firma', firmaFile);
        }
    
        fetch(registrarCarta, {  
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken  
            }
        })
        .then(response => response.json()) 
        .then(data => {
            if (data.status === 'success') {
                showMessageModal('Carta de acceso registrada correctamente');
                document.getElementById('firma').value = '';
                modal1.style.display = 'none';
                location.reload();

            } else {
                showMessageModal('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessageModal('Ocurrió un error inesperado');
        });
    }); 

    tramiteSelect.addEventListener('change', function() {
        if (this.value !== "") {
            opcionesAdicionales.style.display = 'block';
        } else {
            opcionesAdicionales.style.display = 'none';
        }
    });

    verPdfCartaBtn.forEach(function(verPdfCartaBtn) {
        verPdfCartaBtn.addEventListener('click', function() {
            const pdfUrlCarta = this.getAttribute('data-url'); 
            window.open(pdfUrlCarta, '_blank');
        });
    });
    
    cancelUpdate.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    closeModal1.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    registrarTramite.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-autores').style.display = 'block';
        document.getElementById('section-seguimiento').style.display = 'none';

        this.classList.add('active');
        seguimientoTramite.classList.remove('active');
    });

    seguimientoTramite.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-autores').style.display = 'none';
        document.getElementById('section-seguimiento').style.display = 'block';

        this.classList.add('active');
        registrarTramite.classList.remove('active');
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