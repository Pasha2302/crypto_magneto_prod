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
        this.candleSeries.applyOptions({
            lineColor: intervalColors[interval],
        });
        this.chart.timeScale().fitContent();
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
        this.candleSeries = this.chart.addSeries(AreaSeries, {
            topColor: '#2962FF',
            bottomColor: 'rgba(41, 98, 255, 0.28)',
            lineWidth: 2,
            crossHairMarkerVisible: false,
        });
        this.setChartInterval('1D', seriesesData, intervalColors);

        const styles = `
            .buttons-container {
                display: flex;
                flex-direction: row;
                gap: 8px;
            }
            .buttons-container button {
                all: initial;
                font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu,
                    sans-serif;
                font-size: 16px;
                font-style: normal;
                font-weight: 510;
                line-height: 24px; /* 150% */
                letter-spacing: -0.32px;
                padding: 8px 24px;
                color: rgba(19, 23, 34, 1);
                background-color: rgba(240, 243, 250, 1);
                border-radius: 8px;
                cursor: pointer;
            }

            .buttons-container button:hover {
                background-color: rgba(224, 227, 235, 1);
            }

            .buttons-container button:active {
                background-color: rgba(209, 212, 220, 1);
            }
        `;

        const stylesElement = document.createElement('style');
        stylesElement.innerHTML = styles;
        this.container.appendChild(stylesElement);

        const buttonsContainer = document.createElement('div');
        buttonsContainer.classList.add('buttons-container');
        const intervals = ['1D', '1W', '1M', '1Y'];
        intervals.forEach(interval => {
            const button = document.createElement('button');
            button.innerText = interval;
            button.addEventListener('click', () => this.setChartInterval(interval, seriesesData, intervalColors));
            buttonsContainer.appendChild(button);
        });

        this.container.appendChild(buttonsContainer);
    }

    destroy() {
        if (this.chart) {
            this.chart.remove();
            this.chart = null;
        }
    }
}
