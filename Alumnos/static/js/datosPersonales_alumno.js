document.addEventListener('DOMContentLoaded', function (){
    const mostrarDatosPersonales = document.getElementById('mostrar-datos-personales');
    const mostrarConfiguracion = document.getElementById('mostrar-configuracion');
    const updateBtn = document.querySelector('.update-btn');
    const saveBtn = document.querySelector('.save-btn');
    const modal1 = document.getElementById('confirmation-modal1');
    const modal2 = document.getElementById('confirmation-modal2');
    const closeModal1 = document.getElementById('close-modal1');
    const closeModal2 = document.getElementById('close-modal2');
    const confirmUpdate = document.getElementById('confirm-update');
    const cancelUpdate = document.getElementById('cancel-update');
    const confirmChange = document.getElementById('confirm-change');
    const cancelChange = document.getElementById('cancel-change');
    const messageModal = document.getElementById('message-modal');
    const celular = document.getElementById('celular');

    celular.addEventListener('input', function (e) {
        this.value = this.value.replace(/\D/g, '');
        if (this.value.length > 9) {
            this.value = this.value.slice(0, 9);
        }
    });
    
    mostrarDatosPersonales.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-alumno').style.display = 'block';
        document.getElementById('configuracion').style.display = 'none';

        this.classList.add('active');
        mostrarConfiguracion.classList.remove('active');
    });

    mostrarConfiguracion.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('datos-alumno').style.display = 'none';
        document.getElementById('configuracion').style.display = 'block';

        // Cambiar clases activas
        this.classList.add('active');
        mostrarDatosPersonales.classList.remove('active');
    });

    window.togglePassword = function (inputId, toggleIcon) {
        const passwordInput = document.getElementById(inputId);
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        toggleIcon.classList.toggle('fa-eye');
        toggleIcon.classList.toggle('fa-eye-slash');
    };

    updateBtn.addEventListener('click', function () {
        modal1.style.display = 'block';
    });

    cancelUpdate.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    saveBtn.addEventListener('click', function () {
        modal2.style.display = 'block';
    });

    cancelChange.addEventListener('click', function () {
        modal2.style.display = 'none';
    });

    closeModal1.addEventListener('click', function () {
        modal1.style.display = 'none';
    });

    closeModal2.addEventListener('click', function () {
        modal2.style.display = 'none';
    });

    function showMessageModal(message) {
        const messageBody = document.getElementById('message-body');
        messageBody.innerText = message; 
        messageModal.style.display = 'block';

        setTimeout(() => {
            messageModal.style.display = 'none';
            location.reload();
        }, 2000);
    }

    confirmUpdate.addEventListener('click', async function () {
        const email = document.getElementById('email').value;
        const sexo = document.getElementById('sexo').value;
        const fechaNacimiento = document.getElementById('fechaNacimiento').value;
        const domicilio = document.getElementById('domicilio').value;
        const celular = document.getElementById('celular').value;

        const response = await fetch(actualizarDatos, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                alumno_id: alumnoId,
                email: email,
                sexo: sexo,
                fechaNacimiento: fechaNacimiento,
                domicilio: domicilio,
                celular: celular
            })
        });

        if (response.ok) {
            const result = await response.json();
            showMessageModal(result.message);
            modal1.style.display = 'none';
        } else {
            showMessageModal('Error al actualizar los datos.');
        }
    });

    confirmChange.addEventListener('click', async function () {
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const repeatPassword = document.getElementById('repeat-password').value;

        if(newPassword !== repeatPassword){
            showMessageModal('Las nuevas contraseñas no coinciden.');
        }

        const response = await fetch(changePassword, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },

            body: JSON.stringify({
                alumno_id: alumnoId,
                current_password: currentPassword,
                new_password: newPassword
            })
        })

        if (response.ok) {
            const result = await response.json();
            showMessageModal(result.message);
            modal2.style.display = 'none';
            currentPassword.value = '';
            newPassword.value = '';
            repeatPassword.value = '';
        } else {
            showMessageModal('Error al actualizar los datos.');
        } 
    });
});