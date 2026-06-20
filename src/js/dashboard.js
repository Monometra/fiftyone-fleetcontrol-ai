const DATA = {
    totalSamples: 440,
    totalDetections: 8620,
    avgPerSample: 19.6,
    insideManhattan: 141,
    outsideManhattan: 299,
    nearTimesSquare: 134,
    classDistribution: {
        labels: ['car', 'traffic sign', 'traffic light', 'person', 'truck', 'bus', 'motorcycle', 'bicycle'],
        values: [4759, 1579, 1298, 623, 198, 89, 45, 29]
    },
    zoneDensity: {
        labels: ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'],
        values: [141, 98, 87, 72, 42]
    }
};

function animateValue(element, target, suffix = '') {
    let current = 0;
    const step = Math.ceil(target / 40);
    const interval = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(interval);
        }
        element.textContent = current.toLocaleString() + suffix;
    }, 25);
}

function initStats() {
    animateValue(document.getElementById('statSamples'), DATA.totalSamples);
    animateValue(document.getElementById('statDetections'), DATA.totalDetections);
    animateValue(document.getElementById('statInside'), DATA.insideManhattan);
    animateValue(document.getElementById('statNear'), DATA.nearTimesSquare);
}

function initClassChart() {
    const ctx = document.getElementById('classChart').getContext('2d');
    const colors = [
        '#3b82f6', '#8b5cf6', '#f59e0b', '#22c55e',
        '#ef4444', '#ec4899', '#06b6d4', '#f97316'
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: DATA.classDistribution.labels,
            datasets: [{
                label: 'Objetos detectados',
                data: DATA.classDistribution.values,
                backgroundColor: colors.map(c => c + '80'),
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        maxRotation: 45
                    }
                }
            }
        }
    });
}

function initGeoChart() {
    const ctx = document.getElementById('geoChart').getContext('2d');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Dentro Manhattan', 'Fuera Manhattan'],
            datasets: [{
                data: [DATA.insideManhattan, DATA.outsideManhattan],
                backgroundColor: ['#22c55e', '#ef4444'],
                borderColor: ['#166534', '#991b1b'],
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#f1f5f9',
                        padding: 16,
                        font: { size: 13 }
                    }
                }
            }
        }
    });
}

function initDensityChart() {
    const ctx = document.getElementById('densityChart').getContext('2d');
    const colors = ['#3b82f6', '#8b5cf6', '#f59e0b', '#22c55e', '#ef4444'];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: DATA.zoneDensity.labels,
            datasets: [{
                label: 'Capturas por zona',
                data: DATA.zoneDensity.values,
                backgroundColor: colors.map(c => c + '80'),
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initStats();
    initClassChart();
    initGeoChart();
    initDensityChart();
});
