'use strict';
import { ChartConfig } from './tools/config_chart.js';


export class ChartManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.chart = null;
        this.candleSeries = null;

        console.log(
            'has addCandlestickSeries',
            typeof window?.LightweightCharts?.createChart === 'function' && typeof (
                window.LightweightCharts.createChart(document.createElement('div'))?.addCandlestickSeries
            )
        );
        console.log(
            'has addSeries',
            typeof window?.LightweightCharts?.CandlestickSeries, typeof (
                window.LightweightCharts.createChart(document.createElement('div'))?.addSeries
            )
        );
        console.log(
            'LightweightCharts.version()',
            window.LightweightCharts?.version ? window.LightweightCharts.version() : 'no version'
        );

    }

    setChartInterval(interval, seriesesData, intervalColors) {
        this.candleSeries.setData(seriesesData.get(interval));
        this.candleSeries.applyOptions( {lineColor: intervalColors[interval]} );
        this.chart.timeScale().fitContent();   // Автоматически подогнать масштаб по данным
    }

    init(md) {
        const { createChart, LineSeries, AreaSeries } = window.LightweightCharts;
        const seriesesData = new Map([
            ['1D', md.dayData],
            ['1W', md.weekData],
            ['1M', md.monthData],
            ['1Y', md.yearData],
        ]);
        const intervalColors = {
            '1D': '#1cce75ff',
            '1W': 'rgba(165, 216, 47, 1)',
            '1M': 'rgb(242, 142, 44)',
            '1Y': 'rgb(164, 89, 209)',
        };

        this.chart = createChart(this.container, ChartConfig.chart);
        // this.candleSeries = this.chart.addSeries(LineSeries, { color: intervalColors['1D'] });
        this.candleSeries = this.chart.addSeries(AreaSeries, ChartConfig.series);

        this.setChartInterval('1D', seriesesData, intervalColors);

        // Кнопки переключения интервала
        const btns = document.querySelectorAll('.btns-chart-price button');
        btns.forEach( (btn) => {
            const interval = btn.dataset.interval;
            btn.addEventListener('click', () => {
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.setChartInterval(interval, seriesesData, intervalColors)
            });
        });

    }

    destroy() {
        if (this.chart) {
            this.chart.remove();
            this.chart = null;
        }
    }
}
