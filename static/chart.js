'use strict';

fetch('/all_vitals_graph')
    .then((response) => response.json())
    .then((responseJSON) => {
        const data = responseJSON

        const dates = data.dates;
        const systolic = data.systolic;
        const diastolic = data.diastolic;
    })

const bpChart = new Chart(
    document.querySelector('#blood_pressure_chart'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Systolic',
                data: systolic
            },
            {
                label: 'Diastolic',
                data: diastolic
            }]
        }
    }
)

