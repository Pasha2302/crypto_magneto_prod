'use strict';

export class ConverterEventManager {

    constructor(baseEv, apiClientJs = null) {
        this.baseEv = baseEv;

        // Элементы
        this.inputFrom = document.getElementById('converter-amount-from');
        this.inputTo = document.getElementById('converter-amount-to');
        this.selectFrom = document.getElementById('converter-from');
        this.selectTo = document.getElementById('converter-to');
        this.rateBlock = document.getElementById('converter-rate');

        this.init();
    }

    init() {
        this.recalc();  // первый расчёт при загрузке

        this.baseEv.on('click', '#converter-swap', (ev, elm) => this.onSwap(ev, elm));

        this.baseEv.on('input', '#converter-amount-from', () => this.recalc());
        this.baseEv.on('change', '#converter-from', () => this.recalc());
        this.baseEv.on('change', '#converter-to', () => this.recalc());
    }

    // -------------------------------
    // MOCK-API (полностью заменяет сервер)
    // -------------------------------
    async mockConvertRequest({ amount, from, to }) {
        const mockRates = {
            USD: { USD: 1, BTC: 1/43000, ETH: 1/2200, BNB: 1/230, SOL: 1/60 },
            BTC: { USD: 43000, BTC: 1, ETH: 19.5, BNB: 187, SOL: 600 },
            ETH: { USD: 2200, BTC: 1/19.5, ETH: 1, BNB: 9.6, SOL: 30 },
            BNB: { USD: 230, BTC: 1/187, ETH: 1/9.6, BNB: 1, SOL: 3.1 },
            SOL: { USD: 60, BTC: 1/600, ETH: 1/30, BNB: 1/3.1, SOL: 1 }
        };

        const rate = mockRates[from][to];
        const result = (amount * rate).toFixed(8);

        return {
            result,
            rate,
            rate_text: `1 ${from} = ${rate} ${to}`
        };
    }

    // -------------------------------
    // Пересчёт
    // -------------------------------
    async recalc() {
        const amount = Number(this.inputFrom.value) || 0;
        const from = this.selectFrom.value;
        const to = this.selectTo.value;

        try {
            const res = await this.mockConvertRequest({ amount, from, to });

            this.inputTo.value = res.result;
            this.rateBlock.textContent = res.rate_text;

        } catch (err) {
            console.error('[ConverterEventManager.recalc] Error', err);
        }
    }

    // -------------------------------
    // Swap
    // -------------------------------
    onSwap(ev, elm) {
        const prevFrom = this.selectFrom.value;
        const prevTo = this.selectTo.value;

        this.selectFrom.value = prevTo;
        this.selectTo.value = prevFrom;

        const oldFromValue = this.inputFrom.value;
        const oldToValue = this.inputTo.value;

        this.inputFrom.value = oldToValue || 1;
        this.inputTo.value = oldFromValue || '';

        this.recalc();
    }
}
