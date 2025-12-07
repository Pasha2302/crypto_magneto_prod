'use strict';
import { AllEventsManager } from './events/all_events.js';
import { ConverterEventManager } from './events/converter.js';

import { ChartManager } from './charts/chart_coin_price/price_chart_manager.js';
import { DataProviderMock } from './charts/chart_coin_price/tools/data_provider.js';


export function init_page_coin(baseEv, apiClientJs) {
    console.log('\nCoin page script loaded ...');

    new AllEventsManager(baseEv);
    new ConverterEventManager(baseEv,  apiClientJs);

    // Инициализация графика цены монеты:
    const manager = new ChartManager("price-chart");
    const mockData = new DataProviderMock();

    manager.init(mockData.getMockData());
    // manager.setData(mockData.getWeeklyOHLC());
    // ---- //

}
