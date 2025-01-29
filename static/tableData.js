$(document).ready( function () {
    // Se inicializan las DataTables sin la barra de búsqueda
    var tableInventory = $('#inventory-table').DataTable({
        dom: 'ltip' //(l) Selector de longitud, (t) Tabla, (i) Info. tabla, (p) paginación
    });
    var tableHistory = $('#history-table').DataTable({
        dom: 'ltip'
    });

    $('#searchFilter').on('keyup', function() {
        tableInventory.search(this.value).draw();
    });
    $('#searchFilter').on('keyup', function() {
        tableInventory.search(this.value).draw();
    });
} );