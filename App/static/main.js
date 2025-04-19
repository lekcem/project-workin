



async function getUserData2(){
    const response = await fetch('/api/reports');
    return response.json();
}

function loadTable2(reports){
    const table = document.querySelector('#result2');
    for(let report of reports){
        table.innerHTML += `<tr>
            <td>${report.id}</td>
            <td>${report.year}</td>
            <td>${report.campus}</td>
            <td>${report.excelfile}</td>
            <td>
                <button onclick="fetchExcelData(${report.id})">Show Excel Data</button>
                <button onclick="generatePieChart(${report.id})">Generate Pie Chart</button>
                <button onclick="generateBarChart(${report.id})">Generate Bar Chart</button>

            </td>

        </tr>`;
    }
}


function fetchExcelData(reportId) {
    const excelDataContainer = document.querySelector('#excelDataContainer');
    
    if (excelDataContainer.style.display === "none" || excelDataContainer.style.display === "") {
        excelDataContainer.style.display = "block";

        fetch(`/api/exceldata?report_id=${reportId}`)
            .then(response => response.json())
            .then(data => {
                displayExcelData(data);
            })
            .catch(error => {
                console.error('Error fetching Excel data:', error);
            });
    } else {
        excelDataContainer.style.display = "none";
    }
}


function displayExcelData(excelData) {
    const excelDataContainer = document.querySelector('#excelDataContainer');
    excelDataContainer.innerHTML = '';  

    if (excelData.length === 0) {
        excelDataContainer.innerHTML = 'No Excel data found for this report.';
        return;
    }

    let tableHTML = `<table><thead><tr><th>Department</th><th>Students</th></tr></thead><tbody>`;
    for (let data of excelData) {
        tableHTML += `<tr><td>${data.department}</td><td>${data.students}</td></tr>`;
    }
    tableHTML += `</tbody></table>`;

    excelDataContainer.innerHTML = tableHTML;
}


function generatePieChart(reportId) {
    const pieChartCanvas = document.getElementById('pieChart');
    const pieChartContainer = pieChartCanvas.parentElement;

    if (pieChartContainer.style.display === "none" || pieChartContainer.style.display === "") {
        pieChartContainer.style.display = "block";

        fetch(`/api/exceldata?report_id=${reportId}`)
            .then(response => response.json())
            .then(data => {
                const labels = [];
                const studentsData = [];

                data.forEach(entry => {
                    labels.push(entry.department);
                    studentsData.push(entry.students);
                });

                renderPieChart(labels, studentsData);
            })
            .catch(error => {
                console.error('Error fetching Excel data for pie chart:', error);
            });
    } else {
        pieChartContainer.style.display = "none";
    }
}


function renderPieChart(labels, data) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Students',
                data: data,
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFEB33'],
                borderColor: '#FFFFFF',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' students';
                        }
                    }
                }
            }
        }
    });
}

function generateBarChart(reportId) {
    const barChartCanvas = document.getElementById('barChart');
    const barChartContainer = barChartCanvas.parentElement; 

    if (barChartContainer.style.display === "none" || barChartContainer.style.display === "") {
        barChartContainer.style.display = "block";

        fetch(`/api/exceldata?report_id=${reportId}`)
            .then(response => response.json())
            .then(data => {
                const labels = [];
                const studentsData = [];

                data.forEach(entry => {
                    labels.push(entry.department);
                    studentsData.push(entry.students);
                });

                renderBarChart(labels, studentsData);
            })
            .catch(error => {
                console.error('Error fetching Excel data for bar chart:', error);
            });
    } else {
        barChartContainer.style.display = "none";
    }
}


function renderBarChart(labels, data) {
    const ctx = document.getElementById('barChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Students per Department',
                data: data,
                backgroundColor: '#4CAF50', 
                borderColor: '#388E3C',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Departments'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' students';
                        }
                    }
                }
            }
        }
    });
}

async function main(){

    const reports = await getUserData2();
    loadTable2(reports);
}


main();