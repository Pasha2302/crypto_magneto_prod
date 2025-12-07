

export const ChartConfig = {
    chart: {
        height: 500,
        layout: {
            background: { type: 'solid', color: '#1A1B28' },
            textColor: '#ffffff',
        },
        grid: {
            vertLines: { color: '#eee' },
            horzLines: { color: '#eee' },
        },
        timeScale: {
            timeVisible: true,
            secondsVisible: false,
        },
        rightPriceScale: {
            scaleMargins: { top: 0.2, bottom: 0.1 },
        },
    },

    candles: {
        upColor: '#4CAF50',
        downColor: '#E53935',
        borderUpColor: '#4CAF50',
        borderDownColor: '#E53935',
        wickUpColor: '#4CAF50',
        wickDownColor: '#E53935',

    },
};
