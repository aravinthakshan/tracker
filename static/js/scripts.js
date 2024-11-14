function fetchLogs() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("logTable").getElementsByTagName("tbody")[0];
            tableBody.innerHTML = "";
            data.forEach(row => {
                const tr = document.createElement("tr");
                Object.values(row).forEach(cell => {
                    const td = document.createElement("td");
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        })
        .catch(error => console.error("Error fetching logs:", error));
}

setInterval(fetchLogs, 5000); // Update every 5 seconds
document.addEventListener("DOMContentLoaded", fetchLogs);
