$(document).ready( function () {
    var table = $('#inventory-table').DataTable({
        dom: 'ltip'
    });
    $('#history-table').DataTable();
    $('#searchFilter').on('keyup', function() {
        table.search(this.value).draw();
    });
} );