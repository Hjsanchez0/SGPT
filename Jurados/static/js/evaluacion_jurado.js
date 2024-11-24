document.addEventListener('DOMContentLoaded', function () {
    const guardarModal = document.getElementById('guardar-modal');
    const verEnlaceDrive = document.querySelectorAll('.ver-pdf');
    const verObservacion = document.querySelectorAll('.ver-observacion');
    const verDictamen = document.querySelectorAll('.ver-dictamen');
    const semestreSelect = document.getElementById('semestre-select');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');

    semestreSelect.addEventListener('change', function() {
        const semestreId = this.value;
        const semestreNombre = semestreSelect.options[semestreSelect.selectedIndex].text; 

        Array.from(resultadosBusqueda.rows).forEach(row => {
            const semestreCells = row.cells[1]; 
            if (semestreCells) {
                const semestres = semestreCells.innerText.split(', '); 
                const match = semestres.some(semestre => semestre.trim() === semestreNombre); 
                row.style.display = match || row.rowIndex === 0 ? '' : 'none'; 
            }
        });
    });

    verEnlaceDrive.forEach(function(verEnlaceDrive){
        verEnlaceDrive.addEventListener('click', function(){
            const urlDrive = this.getAttribute('data-url');
            window.open(urlDrive, '_blank');
        })
    })

    verObservacion.forEach(function(verObservacion){
        verObservacion.addEventListener('click', function(){
            const urlObs = this.getAttribute('data-url-obs');
            window.open(urlObs, '_blank');
        })
    })

    verDictamen.forEach(function(verDictamen){
        verDictamen.addEventListener('click', function(){
            const urlDrive = this.getAttribute('data-url');
            window.open(urlDrive, '_blank');
        })
    })

    window.addEventListener('click', function(event) {
        if (event.target === guardarModal) {
            guardarModal.style.display = 'none';
        }
    });
});
