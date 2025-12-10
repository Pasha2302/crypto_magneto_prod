'use strict';
import { AllEventsManager } from './events/all_events.js';
import { ConverterEventManager } from './events/converter.js';

import { ChartManager } from './charts/chart_coin_price/price_chart_manager.js';
import { DataProviderMock } from './charts/chart_coin_price/tools/data_provider.js';


function createChartTokenomics() {
    const data = JSON.parse(
        document.getElementById('chart-tokenomics-mocke-json').textContent
    );

    data.values = data.values.map(Number);

    const Chart = window.Chart;
    const ctx = document.getElementById('tokenomics-chart').getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(153, 102, 255, 0.6)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 14
                    },
                    formatter: function(value, ctx) {
                        const total = ctx.chart.data.datasets[0].data
                            .reduce((a, b) => a + b, 0);
                        const percent = (value / total * 100).toFixed(1);
                        return `${percent}%`;  // ← текст на диаграмме
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            const value = ctx.raw;
                            const total = ctx.dataset.data.reduce((a,b)=>a+b,0);
                            const percent = (value / total * 100).toFixed(1);
                            return `${ctx.label}: ${value.toLocaleString()} (${percent}%)`;
                        }
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}




export function init_page_coin(baseEv, apiClientJs) {
    console.log('\nCoin page script loaded ...');

    new AllEventsManager(baseEv);
    new ConverterEventManager(baseEv,  apiClientJs);

    // Инициализация графика цены монеты:
    const manager = new ChartManager("price-chart");
    const mockData = new DataProviderMock();
    manager.init(mockData.getMockData());
    // ---- //

    // Инициализация круговой диаграммы токеномики:
    createChartTokenomics();

}
