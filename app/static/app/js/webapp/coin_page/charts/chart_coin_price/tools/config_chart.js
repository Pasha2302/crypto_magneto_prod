

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
            timeVisible: true,
            secondsVisible: false,
        },

        rightPriceScale: {
            scaleMargins: {
                top: 0.3,  // Оставить немного места для легенды
                bottom: 0.1
            },
        },
    },
};
