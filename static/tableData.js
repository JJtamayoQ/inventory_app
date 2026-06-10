$(document).ready(function () {
    const tableIds = [
        '#inventory-table',
        '#history-table',
        '#inactive-table',
        '#workers-table',
        '#inactive_workers-table'
    ];

    const tables = tableIds
        .filter(selector => $(selector).length)
        .map(selector => $(selector).DataTable({
            dom: 'ltip'
        }));

    $('#searchFilter').on('keyup', function () {
        tables.forEach(table => table.search(this.value).draw());
    });
});
