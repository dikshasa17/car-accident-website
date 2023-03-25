const lineChart = (chartLabel, canvas, labels, items, borderColor) => {
    const chart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                label: chartLabel,
                data: items,
                fill: false,
                borderColor: borderColor,
                tension: 0.1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        max: 1,
                        stepSize: 1,
                        callback: function(value, index, values) {
                            if (value === 0) {
                                return 'False';
                            } 
                            else if (value === 1){
                                return 'True';
                            }
                            else {
                                return '';
                            }
                        }
                    },
                },
                x: {
                    ticks: {
                    maxRotation: 45,
                    minRotation: 45
                    }
                }
            },
            animation: {
                duration: 0
            },
        },
    });

    return chart;
}