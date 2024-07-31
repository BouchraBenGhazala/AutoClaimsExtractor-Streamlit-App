severity_colors = {
    0: "#FFFFFF",
    1: "#FFFF00",
    2: "#FFA500",
    3: "#FF0000",
};

var paths = document.querySelectorAll("[data-name]");
paths.forEach(function (path) {
    path.setAttribute('data-severity', 0);
});

paths.forEach(function (path) {
    path.addEventListener("click", function () {
        var severity = parseInt(path.getAttribute('data-severity'));
        var part_name = path.dataset.name;
        if (severity < 3) {
            path.style.fill = severity_colors[severity + 1];
            path.setAttribute('data-severity', severity + 1);
            document.getElementById("details-box").innerHTML = part_name + " - " + (severity + 1);
        }
        else if (severity == 3) {
            path.style.fill = severity_colors[0];
            path.setAttribute('data-severity', 0);
            document.getElementById("details-box").innerHTML = part_name + " - " + 0;
        }
        updateTable();
    });
});

paths.forEach(function (path) {
    path.addEventListener("contextmenu", function (e) {
        e.preventDefault();
        var severity = parseInt(path.getAttribute('data-severity'));
        var part_name = path.dataset.name;
        if (severity > 0) {
            path.style.fill = severity_colors[severity - 1];
            path.setAttribute('data-severity', severity - 1);
            document.getElementById("details-box").innerHTML = part_name + " - " + (severity - 1);
        }
        else if (severity == 0) {
            path.style.fill = severity_colors[3];
            path.setAttribute('data-severity', 3);
            document.getElementById("details-box").innerHTML = part_name + " - " + 3;
        }
        updateTable();
    });
});

for (var key in damaged_parts) {
    try {
        var path = document.querySelector("[data-name='" + unescape(encodeURIComponent(key)) + "']");
        var severity = damaged_parts[key];
        if (severity == 1) {
            path.style.fill = severity_colors[1];
            path.setAttribute('data-severity', severity);
        }
        else if (severity == 2) {
            path.style.fill = severity_colors[2];
            path.setAttribute('data-severity', severity);
        }
        else if (severity == 3) {
            path.style.fill = severity_colors[3];
            path.setAttribute('data-severity', severity);
        }
    }
    catch (error) {
        console.log("Error: " + key);
    }
}

function getDamagedParts() {
    var damaged_parts = {};
    paths.forEach(function (path) {
        var severity = parseInt(path.getAttribute('data-severity'));
        var part_name = path.dataset.name;
        if (severity != 0) {
            damaged_parts[part_name] = severity;
        }
    });
    return damaged_parts;
}

function updateTotalTable() {
    var res_table = document.getElementById('res-table');
    var total_table = document.getElementById('total-table');
    total_table.innerHTML = "<tr><th>Total</th><th>Total - Franchise</th><th>Total / 2</th></tr>";
    var total_cost = 0;
    // loop through all the last cells of the rows
    for (var i = 1; i < res_table.rows.length; i++) {
        total_cost += parseInt(res_table.rows[i].cells[3].innerHTML.split(" ")[0]);
    }
    // also add parts from the add-table
    var add_table = document.getElementById('add-table');
    for (var i = 1; i < add_table.rows.length; i++) {
        total_cost += parseInt(add_table.rows[i].cells[3].innerHTML.split(" ")[0]);
    }
    total_fr = total_cost - 500; // total - franchise
    total2 = total_cost / 2; // total / 2
    var row = total_table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = total_cost + " Dhs";
    cell2.innerHTML = total_fr + " Dhs";
    cell3.innerHTML = total2 + " Dhs";
}

function updateTable() {
    var res_table = document.getElementById('res-table');
    var damaged_parts = getDamagedParts();
    // sort damaged_parts by severity
    // damaged_parts = Object.fromEntries(Object.entries(damaged_parts).sort(([, a], [, b]) => b - a));
    res_table.innerHTML = "<tr><th>Part Name</th><th>Severity</th><th>Decision</th><th>Cost</th></tr>";
    for (var key in damaged_parts) {
        var row = res_table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = key;
        cell2.innerHTML = damaged_parts[key];
        if (damaged_parts[key] < 3) {
            cell3.innerHTML = "Repair";
        }
        else if (damaged_parts[key] == 3) {
            cell3.innerHTML = "Replace";
        }
        cell4.innerHTML = prix_dict[key][damaged_parts[key]-1] + " Dhs";
    }
    updateTotalTable();
}
updateTable();

var add_table = document.getElementById('add-table');
add_table.innerHTML = "<tr></tr>";    

add_button = document.getElementById('add-damage');
add_button.addEventListener('click', function () {
    var row = add_table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var part_select = document.createElement("select");
    part_select.id = "part-select";
    for (var key in prix_add_dict) {
        var option = document.createElement("option");
        option.text = key;
        part_select.add(option);
    }
    var severity_input = document.createElement("select");
    severity_input.id = "severity-input";
    for (var i = 1; i <= 3; i++) {
        var option = document.createElement("option");
        option.text = i;
        severity_input.add(option);
    }
    cell1.innerHTML = part_select.outerHTML;
    cell2.innerHTML = severity_input.outerHTML;
    cell3.innerHTML = "Repair";
    cell4.innerHTML = prix_add_dict[part_select.value][severity_input.value-1] + " Dhs";
    updateTotalTable();
});

document.addEventListener('change', function (e) {
    if (e.target.id == "part-select" || e.target.id == "severity-input") {
        if (e.target.id == "part-select") {
            var part_name = e.target.value;
            var severity_input = e.target.parentElement.nextElementSibling.firstChild;
            var decision = e.target.parentElement.nextElementSibling.nextElementSibling;
        }
        else if (e.target.id == "severity-input") {
            var part_name = e.target.parentElement.previousElementSibling.firstChild.value;
            var severity_input = e.target;
            var decision = e.target.parentElement.nextElementSibling;
        }
        if (severity_input.value < 3) {
            decision.innerHTML = "Repair";
        }
        else if (severity_input.value == 3) {
            decision.innerHTML = "Replace";
        }
        var cost = prix_add_dict[part_name][severity_input.value-1];
        decision.nextElementSibling.innerHTML = cost + " Dhs";
        updateTotalTable();
    }
});


var tooltipSpan = document.getElementById('details-box');
document.addEventListener('mouseover', function (e) {
    if (e.target.tagName == 'path') {
        var severity = parseInt(e.target.getAttribute('data-severity'));
        var part_name = e.target.dataset.name;
        if (part_name == undefined) {
            document.getElementById("details-box").style.opacity = "0%";
        }
        else {
            document.getElementById("details-box").innerHTML = part_name + " - " + severity;
            document.getElementById("details-box").style.opacity = "100%";
            document.getElementById("details-box").style.display = "block";
        }
    }
    else {
        document.getElementById("details-box").style.opacity = "0%";
    }
});

window.onmousemove = function (e) {
    var x = e.clientX,
        y = e.clientY;
    tooltipSpan.style.top = (y + 20) + 'px';
    tooltipSpan.style.left = (x) + 'px';
};