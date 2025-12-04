'use strict';
import { AllEventsManager } from './events/all_events.js';
import { ConverterEventManager } from './events/converter.js';


export function init_page_coin(baseEv, apiClientJs) {
    console.log('\nCoin page script loaded ...');

    new AllEventsManager(baseEv);
    new ConverterEventManager(baseEv,  apiClientJs);
}
