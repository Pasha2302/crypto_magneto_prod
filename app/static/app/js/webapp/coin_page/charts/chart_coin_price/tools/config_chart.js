

export const ChartConfig = {
    chart: {
        height: 500,
        layout: {
            background: { type: 'solid', color: '#1A1B28' },
            textColor: '#ffffff',
        },

        // Скрыть линии сетки
        grid: {
            vertLines: {
                visible: false,
            },
            horzLines: {
                visible: false,
            },
        },

        timeScale: {
            timeVisible: false,
            secondsVisible: false,
        },

        rightPriceScale: {
            scaleMargins: {
                top: 0.3,  // Оставить немного места для легенды
                bottom: 0.1
            },
        },
    },

    series: {
        topColor: '#2962FF',
        bottomColor: 'rgba(41, 98, 255, 0.28)',
        lineWidth: 2,
        crossHairMarkerVisible: false,

        priceFormat: {
            type: 'price',
            precision: 8,       // количество знаков после запятой
            minMove: 0.00000001 // минимальный шаг
        }
    },

};
