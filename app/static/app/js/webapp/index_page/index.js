'use strict';
import { TableFilterEventManager } from './events/table_filters.js';


export function init_page_index(baseEv, apiClientJs) {
    console.log('\nIndex page script loaded ...');

    new TableFilterEventManager(baseEv, apiClientJs);

}