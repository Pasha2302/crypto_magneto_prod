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


document.addEventListener('DOMContentLoaded', () => {
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
        import('../index_page/index.js').then( ({ init_page_index }) => {
            init_page_index(baseEv, apiClientJs);
        });

    } else if ( namePage === 'page_coin' ) {
        import('../coin_page/coin.js').then( ({ init_page_coin }) => {
            init_page_coin(baseEv, apiClientJs);
        });

    } else if ( namePage === 'add_coin' ) {
        import('../add_coin_page/add_coin.js').then( ({ init_add_coin_page }) => {
            init_add_coin_page(baseEv, apiClientJs);
        });
    }

});
