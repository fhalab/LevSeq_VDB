function loadTable(data) {
    new DataTable('#myTable', {
        columns: data.columns,
        data: data.rows,
        dom: 'Bfrtip',
        columnDefs: [ { "defaultContent": "-", "targets": "_all" } ],
        buttons: ['csv', 'excel']
    });
}
