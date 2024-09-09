function loadTable(data) {
    new DataTable('#myTable', {
        columns: data.columns,
        data: data.rows,
        dom: 'Bfrtip',
        buttons: ['csv', 'excel']
    });
}
