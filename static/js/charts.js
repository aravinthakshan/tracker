let timeChart;

function updateChart(data) {
    if (timeChart) {
        timeChart.destroy();
    }

    const ctx = document.getElementById("timeChart").getContext("2d");
    timeChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF",
                    "#FF9F40"
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
}

function fetchTimeDistribution() {
    fetch("/time_distribution")
        .then(response => response.json())
        .then(data => updateChart(data))
        .catch(error => console.error("Error fetching time distribution:", error));
}

setInterval(fetchTimeDistribution, 5000); // Update every 5 seconds
document.addEventListener("DOMContentLoaded", fetchTimeDistribution);
