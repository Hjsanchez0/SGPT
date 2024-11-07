document.addEventListener('DOMContentLoaded', function (){
    const mostrarDatosAutores = document.getElementById('mostrar-datos-autores');
    const datosInvestigacion = document.getElementById('datos-investigacion');
    const nextBtn = document.querySelector('.next-btn');
    const backBtn = document.getElementById('back-btn');
    const messageModal = document.getElementById('message-modal');
    const buscarBtn = document.getElementById('buscar-btn');
    const buscarDNI = document.getElementById('buscar-dni');
    const buscarCodMatricula = document.getElementById('buscar-codMatricula');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');
    const rucInput = document.getElementById('ruc-input');
    const saveBtn = document.querySelector('.save-btn');
    const confirmUpdate = document.getElementById('confirm-update');
    const modal1 = document.getElementById('confirmation-modal1');
    const cancelUpdate = document.getElementById('cancel-update');
    const closeModal1 = document.getElementById('close-modal1');

    let currentDNI = ''; 
    let currentCodMatricula = '';

    saveBtn.addEventListener('click', function () {
        const titulo = document.getElementById('titulo').value.trim();
        const institucion = document.getElementById('institucion').value.trim();
        const ruc = rucInput.value.trim();
        const director = document.getElementById('director').value.trim();
        const cargo = document.getElementById('cargo').value.trim();
        const direccion = document.getElementById('direccion').value.trim();

        if (!titulo || !institucion || !ruc || !director || !cargo || !direccion) {
            showMessageModal('Por favor, completa todos los campos antes de guardar la información.');
            return; 
        }

        modal1.style.display = 'block';
    });

    cancelUpdate.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    closeModal1.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    rucInput.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '');
        if (this.value.length > 15) {
            this.value = this.value.slice(0, 15);
        }
    });

    buscarDNI.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '');
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }
    });

    buscarCodMatricula.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '');
        if (this.value.length > 12) {
            this.value = this.value.slice(0, 12);
        }
    });

    mostrarDatosAutores.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-autores').style.display = 'block';
        document.getElementById('investigacion').style.display = 'none';

        this.classList.add('active');
        datosInvestigacion.classList.remove('active');
    });

    datosInvestigacion.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-autores').style.display = 'none';
        document.getElementById('investigacion').style.display = 'block';

        this.classList.add('active');
        mostrarDatosAutores.classList.remove('active');
    });

    nextBtn.addEventListener('click', function () {
        document.getElementById('datos-autores').style.display = 'none';
        document.getElementById('investigacion').style.display = 'block';

        datosInvestigacion.classList.add('active');
        mostrarDatosAutores.classList.remove('active');
    });

    backBtn.addEventListener('click', function () {
        document.getElementById('investigacion').style.display = 'none';
        document.getElementById('datos-autores').style.display = 'block';

        mostrarDatosAutores.classList.add('active');
        datosInvestigacion.classList.remove('active');
    });

    function showMessageModal(message) {
        const messageBody = document.getElementById('message-body');
        messageBody.innerText = message; 
        messageModal.style.display = 'block';

        setTimeout(function() {
            messageModal.style.display = 'none';
        }, 1500);
    }

    function handleCheckboxChange(event) {
        const checkbox = event.target;
    
        if (checkbox.checked) {
            showMessageModal('El estudiante ha sido agregado.'); 
        } else {
            showMessageModal('El estudiante ha sido eliminado.');
        }
    }

    function addCheckboxEventListeners() {
        const checkboxes = document.querySelectorAll('.select-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', handleCheckboxChange);
        });
    }

    buscarBtn.addEventListener('click', function () {
        const dni = buscarDNI.value.trim();
        const codMatricula = buscarCodMatricula.value.trim();
        if (!dni && !codMatricula) {
            showMessageModal('Por favor, ingresa al menos un campo: DNI o Código de Matrícula.');
            return;
        }
    
        fetch(buscarEstudiante, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({ dni: dni, codMatricula: codMatricula })
        })
        .then(response => response.json())
        .then(data => {
            resultadosBusqueda.innerHTML = '';
            let found = false;

            data.resultados.forEach((estudiante, index) => { 
                if (estudiante.dni !== currentDNI && estudiante.codMatricula !== currentCodMatricula) {
                    resultadosBusqueda.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${estudiante.dni}</td>
                            <td>${estudiante.codMatricula}</td>
                            <td>${estudiante.apellidoPat} ${estudiante.apellidoMat}</td>
                            <td>${estudiante.nombres}</td>
                            <td>
                                ${estudiante.omitir_botones ? '' : `
                                    <input type="checkbox" name="select-estudiante" class="select-checkbox" value="${estudiante.id}">
                                `}
                            </td>
                        </tr>
                    `;
                    found = true;
                }
            });
    
            if (!found) {
                resultadosBusqueda.innerHTML += `<tr><td colspan="6">No se encontraron estudiantes.</td></tr>`;
            }
    
            buscarDNI.value = '';
            buscarCodMatricula.value = '';
            addCheckboxEventListeners();
        })
        .catch(error => {
            console.error('Error:', error);
            resultadosBusqueda.innerHTML = `<tr><td colspan="6">Ocurrió un error al buscar.</td></tr>`;
        });
    });

    confirmUpdate.addEventListener('click', function(){
        const semestre = document.getElementById('semestre-select').value;
        const institucion = document.getElementById('institucion').value;
        const ruc = document.getElementById('ruc-input').value;
        const titulo = document.getElementById('titulo').value;
        const director = document.getElementById('director').value;
        const cargo = document.getElementById('cargo').value;
        const direccion = document.getElementById('direccion').value;
        const selectedCheckboxes = document.querySelectorAll('input[name="select-estudiante"]:checked');
        const selectedIds = Array.from(selectedCheckboxes).map(checkbox => checkbox.value); 

        fetch(guardarInvestigacion, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({
                alumno_id: alumnoId,
                semestre_id: semestre,
                institucion: institucion,
                ruc: ruc,
                titulo: titulo,
                director: director,
                cargo: cargo,
                direccion: direccion,
                selected_ids: selectedIds
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                modal1.style.display = 'none';
                showMessageModal(data.message)
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                modal1.style.display = 'none';
                showMessageModal(data.message) 
            }
        })
        .catch(error => console.error('Error:', error));
    });
});