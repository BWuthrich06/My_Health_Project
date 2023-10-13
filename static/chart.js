'use strict';

fetch('/all_vitals_graph')
    .then((response) => response.json())
    .then((responseJSON) => {
        const vitals = responseJSON.vitals;

        const dates = [];
        const systolic = [];
        const diastolic = [];
        const heart_rate = []
        const oxygen = []
        const weight = []
        const glucose = []

        for (const vital of vitals) {
            dates.push(vital.date_time);
            systolic.push(vital.systolic);
            diastolic.push(vital.diastolic);
            heart_rate.push(vital.heart_rate);
            oxygen.push(vital.oxygen);
            weight.push(vital.weight);
            glucose.push(vital.glucose);
        }

    

        let bpChart = new Chart(
            document.querySelector('#blood_pressure_chart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Systolic',
                        data: systolic,
                        backgroundColor: 'rgba(237, 82, 15, 0.92)',
                        borderColor: 'rgba(237, 82, 15, 0.92)',
                        },
                        {
                        label: 'Diastolic',
                        data: diastolic,
                        backgroundColor: 'rgba(237, 168, 24, 0.92)',
                        borderColor: 'rgba(237, 168, 24, 0.92)',
                        }]
                    },
               
                }
            )


        let heartRateChart = new Chart(
            document.querySelector('#heart_rate_chart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Heart Rate',
                        data: heart_rate,
                        backgroundColor: 'rgba(23, 204, 85, 0.93)',
                        borderColor: 'rgba(23, 204, 85, 0.93)',
                        }] 
                    },
             
                })




        let oxygenChart = new Chart(
            document.querySelector('#oxygen_chart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Oxgyen',
                        data: oxygen,
                        backgroundColor: 'rgba(27, 52, 124, 0.93)',
                        borderColor: 'rgba(27, 52, 124, 0.93)',
                        }] 
                    },
               
                })



        let weightChart = new Chart(
            document.querySelector('#weight_chart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Weight',
                        data: weight,
                        backgroundColor: 'rgba(40, 182, 208, 0.91)',
                        borderColor: 'rgba(40, 182, 208, 0.91)',
                        }] 
                    },
             
                })


        
        let glucoseChart = new Chart(
            document.querySelector('#glucose_chart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Glucose',
                        data: glucose,
                        backgroundColor: 'rgba(101, 84, 192, 0.84)',
                        borderColor: 'rgba(101, 84, 192, 0.84)',
                        }] 
                    },
               
                })

});
