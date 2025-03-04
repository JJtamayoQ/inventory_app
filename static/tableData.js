$(document).ready( function () {
    // Se inicializan las DataTables sin la barra de búsqueda
    var tableInventory = $('#inventory-table').DataTable({
        dom: 'ltip' //(l) Selector de longitud, (t) Tabla, (i) Info. tabla, (p) paginación
    });
    var tableHistory = $('#history-table').DataTable({
        dom: 'ltip'
    });
    var tableInactive = $('#inactive-table').DataTable({
        dom: 'ltip'
    });
    var tableWorkers = $('#workers-table').DataTable({
        dom: 'ltip'
    });
    var tableInactiveWorkers = $('#inactive_workers-table').DataTable({
        dom: 'ltip'
    });

    $('#searchFilter').on('keyup', function() {
        tableInventory.search(this.value).draw();
    });
    $('#searchFilter').on('keyup', function() {
        tableHistory.search(this.value).draw();
    });
    $('#searchFilter').on('keyup', function() {
        tableInactive.search(this.value).draw();
    });
    $('#searchFilter').on('keyup', function() {
        tableWorkers.search(this.value).draw();
    });
    $('#searchFilter').on('keyup', function() {
        tableInactiveWorkers.search(this.value).draw();
    });
} );