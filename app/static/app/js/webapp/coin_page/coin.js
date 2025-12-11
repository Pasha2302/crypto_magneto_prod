'use strict';
import { AllEventsManager } from './events/all_events.js';
import { ConverterEventManager } from './events/converter.js';

import { ChartManager } from './charts/chart_coin_price/price_chart_manager.js';
import { DataProviderMock } from './charts/chart_coin_price/tools/data_provider.js';


function createChartTokenomics() {
    const data = JSON.parse(
        document.getElementById('pie_chart_data-json').textContent
    );

    data.values = data.values.map(Number);
    window.pieChartData = data;

    const Chart = window.Chart;
    const ctx = document.getElementById('tokenomics-chart').getContext('2d');

    // Генерация красивых цветов под любое количество сегментов
    const colors = [
        'rgba(75, 192, 192, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 205, 86, 0.7)',
        'rgba(201, 203, 207, 0.7)',
        'rgba(54, 162, 235, 0.7)',
    ];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,   // <-- Готовые проценты
                backgroundColor: colors.slice(0, data.values.length),
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
                    textAlign: 'center',
                    formatter: function(value, ctx) {
                        const label = ctx.chart.data.labels[ctx.dataIndex];
                        return `${label}\n${value}%`;   // <-- Прямо на пироге
                    }
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(ctx) {
                            return `${ctx.label}: ${ctx.raw}%`;
                        }
                    }
                },
                legend: {
                    position: 'left'
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
