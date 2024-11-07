document.addEventListener('DOMContentLoaded', function () {
    const semestreSelect = document.getElementById('semestre-select');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');
    const dniInput = document.getElementById('buscar-dni'); 
    const buscarBtn = document.getElementById('buscar-btn');

    buscarBtn.addEventListener('click', function() {
        const dniIngresado = dniInput.value.trim(); 
        
        Array.from(resultadosBusqueda.rows).forEach(row => {
            const dniCell = row.cells[3]; // La celda del DNI
            if (dniCell) {
                const dniTexto = dniCell.innerText.trim();
                const dniList = dniTexto.split(' - '); // Separar por guiones para múltiples DNIs
                const match = dniList.some(dni => dni.trim() === dniIngresado);
                row.style.display = match || row.rowIndex === 0 ? '' : 'none'; // Mostrar fila si hay coincidencia
            }
        });
    });
    
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
});
