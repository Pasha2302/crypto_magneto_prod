'use strict';
import { BaseEvent } from '../../tools/event_manager.js';
import { RequestJs } from '../../tools/request.js';
import { MobileMenu } from './events/mobile_menu.js';
import { MainInputSearch } from './events/input_search.js';


function updateViewportUnits() {
    // 1vh = 1% от реальной высоты окна
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);

    // 1vw = 1% от реальной ширины окна
    let vw = window.innerWidth * 0.01;
    document.documentElement.style.setProperty("--vw", `${vw}px`);
}


document.addEventListener('DOMContentLoaded', async () => {
    const namePage = document.body.dataset.page;
    console.log(`\nMain script loaded ... Page: ${namePage}`);

    // Установка vh vw для мобильных устройств
    updateViewportUnits();
    window.addEventListener("resize", () => updateViewportUnits());

    // -----
    const apiClientJs = new RequestJs({baseUrl: window.location.origin + '/api-app-v1/'});
    const baseEv = new BaseEvent();
    baseEv.attachDOMEvents();
    
    new MobileMenu(baseEv);
    new MainInputSearch(baseEv, apiClientJs);

    // -----

    if ( namePage === 'index' ) {
        const { init_page_index } = await import('../index_page/index.js');
        init_page_index(baseEv, apiClientJs);

    } else if ( namePage === 'page_coin' ) {
        await import('../../node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.js');
        console.log('Lightweight Charts loaded');

        // Правильный импорт Chart.js UMD
        await import('../../node_modules/chart.js/dist/chart.umd.min.js');
        await import('https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2');
        console.log('Chart.js loaded');

        const { init_page_coin } = await import('../coin_page/coin.js');
        init_page_coin(baseEv, apiClientJs);

    } else if ( namePage === 'add_coin' ) {
        const { init_add_coin_page } = await import('../add_coin_page/add_coin.js');
        init_add_coin_page(baseEv, apiClientJs);
    }

});
