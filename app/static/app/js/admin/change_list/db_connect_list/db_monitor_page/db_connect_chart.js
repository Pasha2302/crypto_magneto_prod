'use strict';

let currentRange = 'day';
let activeChart, idleChart;


// Переключение диапазона
function updateRange(range) {
    currentRange = range;

    document.querySelectorAll('.range-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.range-btn[data-range="${range}"]`).classList.add('active');

    renderCharts(range);
}


function formatLabel(timestamp, range) {
    const date = new Date(timestamp);
    if (range === 'day') {
        // часы:минуты
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (range === 'week') {
        // день и месяц
        return date.toLocaleDateString([], { day: '2-digit', month: 'short' });
    } else if (range === 'month') {
        // день, месяц и год
        return date.toLocaleDateString([], { day: '2-digit', month: 'short', year: 'numeric' });
    }
    return timestamp;
}


function renderCharts(range) {
    const data = snapshots[range];
    if (!data || data.length === 0) return;

    const labels = data.map( s => formatLabel(s.timestamp, range) );
    const active = data.map(s => s.active);
    const idle = data.map(s => s.idle);

    const ctxActive = document.getElementById('activeChart').getContext('2d');
    const ctxIdle = document.getElementById('idleChart').getContext('2d');

    if (activeChart) activeChart.destroy();
    if (idleChart) idleChart.destroy();

    const day_ticks = {
        callback: function (value, index) {
            // Показываем только каждую 3-ю подпись
            return index % 3 === 0 ? this.getLabelForValue(value) : '';
        },
        maxRotation: 45,
        minRotation: 0
    }
    
    const ticks = range === 'day' ? day_ticks : {};
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            title: { display: false },
            tooltip: { mode: 'index', intersect: false }
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
        scales: {
            x: {
                display: true,
                title: { display: true, text: 'Time' },
                ticks,

            },
            y: { beginAtZero: true, suggestedMax: Math.max(...active) * 1.1 }
        }
    }

    console.log('\nLabels:', labels);
    activeChart = new Chart(ctxActive, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Active',
                data: active,
                tension: 0.2,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0,123,255,0.1)',
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options,
    });

    options.scales.y.suggestedMax = Math.max(...idle) * 1.1;
    idleChart = new Chart(ctxIdle, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Idle',
                data: idle,
                tension: 0.2,
                borderColor: '#fd7e14',
                backgroundColor: 'rgba(253,126,20,0.1)',
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options,
    });
}


document.addEventListener('DOMContentLoaded', () => {
    renderCharts(currentRange);
});
