function addRow() {
        var table = document.getElementById("travel_details_table");
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);

        cell1.innerHTML = '<input type="text" name="travel_place[]" class="form-control" placeholder="Travel Place" required="1"/>';
        cell2.innerHTML = '<input type="text" name="place_description[]" class="form-control" placeholder="Place Description" required="1"/>';
        cell3.innerHTML = '<button class="btn btn-danger btn-sm" onclick="removeRow(this)">Remove</button>';
    }

    function removeRow(btn) {
        var row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }

    var currentDate = new Date().toISOString().slice(0, 10);

    document.getElementById("request_date").value = currentDate;

function goBack() {
  window.history.back()
}