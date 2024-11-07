document.addEventListener('DOMContentLoaded', function () {
    const guardarModal = document.getElementById('guardar-modal');
    const terminarBtn = document.querySelector('.btn-terminar');
    const closeModal = document.getElementById("close-guardar-modal");
    const cancelarBtn = document.getElementById("cancelar-guardar");
    const confirmBtn = document.getElementById("confirmar-guardar");
    const messageModal = document.getElementById('message-modal');

    terminarBtn.addEventListener("click", function() {
        guardarModal.style.display = 'block';
    });
    
    closeModal.addEventListener("click", function() {
        guardarModal.style.display = 'none';
    });
    
    cancelarBtn.addEventListener("click", function() {
        guardarModal.style.display = 'none';
    });

    confirmBtn.addEventListener("click", function() {
        const redirectUrl = confirmBtn.getAttribute("data-redirect-url");
        const form1 = new FormData(document.getElementById("evaluacion-form"));
        const form2 = new FormData(document.getElementById("evaluacion-form2"));

        const introduccionRadios = document.getElementsByName("calificacion_introduccion");
        const introduccionSeleccionado = Array.from(introduccionRadios).some(radio => radio.checked);
        const antecedentesRadios = document.getElementsByName("calificacion_antecedentes");
        const antecedentesSeleccionado = Array.from(antecedentesRadios).some(radio => radio.checked);
        const marcoTeoricoRadios = document.getElementsByName("calificacion_marco_teorico");
        const marcoTeoricoSeleccionado = Array.from(marcoTeoricoRadios).some(radio => radio.checked);
        const hipotesisRadios = document.getElementsByName("calificacion_hipotesis");
        const hipotesisSeleccionado = Array.from(hipotesisRadios).some(radio => radio.checked);
        const metodologiaRadios = document.getElementsByName("calificacion_metodologia");
        const metodologiaSeleccionado = Array.from(metodologiaRadios).some(radio => radio.checked);
        const aspectosAdministrativosRadios = document.getElementsByName("calificacion_aspectos_administrativos");
        const aspectosAdministrativosSeleccionado = Array.from(aspectosAdministrativosRadios).some(radio => radio.checked);
        const redaccionRadios = document.getElementsByName("calificacion_redaccion");
        const redaccionSeleccionado = Array.from(redaccionRadios).some(radio => radio.checked);
        const citaReferenciaRadios = document.getElementsByName("calificacion_citayreferencia");
        const citaReferenciaSeleccionado = Array.from(citaReferenciaRadios).some(radio => radio.checked);


        if (!introduccionSeleccionado || !antecedentesSeleccionado || !marcoTeoricoSeleccionado || !hipotesisSeleccionado || !metodologiaSeleccionado || !aspectosAdministrativosSeleccionado || !redaccionSeleccionado || !citaReferenciaSeleccionado) {
            guardarModal.style.display = 'none';
            showMessageModal("Por favor, debe seleccionar todas las calificaciones");
            return; 
        }

        const data = {
            asignacionId: asignacionId, 
            calificacion_introduccion: form1.get("calificacion_introduccion"),
            observacion_introduccion: form1.get("observacion_introduccion"),
            calificacion_antecedentes: form1.get("calificacion_antecedentes"),
            observacion_antecedentes: form1.get("observacion_antecedentes"),
            calificacion_marco_teorico: form1.get("calificacion_marco_teorico"),
            observacion_marco_teorico: form1.get("observacion_marco_teorico"),
            calificacion_hipotesis: form1.get("calificacion_hipotesis"),
            observacion_hipotesis: form1.get("observacion_hipotesis"),
            calificacion_metodologia: form1.get("calificacion_metodologia"),
            observacion_metodologia: form1.get("observacion_metodologia"),
            calificacion_aspectos_administrativos: form1.get("calificacion_aspectos_administrativos"),
            observacion_aspectos_administrativos: form1.get("observacion_aspectos_administrativos"),

            calificacion_redaccion: form2.get("calificacion_redaccion"),
            observacion_redaccion: form2.get("observacion_redaccion"),
            calificacion_citayreferencia: form2.get("calificacion_citayreferencia"),
            observacion_citayreferencia: form2.get("observacion_citayreferencia"),
        };
        fetch(guardarEvaluacion, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            setTimeout(() => {
                guardarModal.style.display = 'none';
                showMessageModal('Evaluación guardada', result);
                window.location.href = redirectUrl;
            }, 1500);
        })
        .catch(error => console.error('Error:', error));

    });

    window.addEventListener('click', function(event) {
        if (event.target === guardarModal) {
            guardarModal.style.display = 'none';
        }
    });

    function showMessageModal(message) {
        const messageBody = document.getElementById('message-body');
        messageBody.innerText = message; 
        messageModal.style.display = 'block';

        setTimeout(() => {
            messageModal.style.display = 'none';
        }, 1500);
    }
});
