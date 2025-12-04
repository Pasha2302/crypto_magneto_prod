'use strict';
import { BaseEvent } from '../../tools/event_manager.js';
import { RequestJs } from '../../tools/request.js';

import { enableImageOverlay } from './tools/image_management.js';
import { setJSONBlocks } from './tools/json_view_dj.js';
import { SelectionEventsImage } from './events/select_preview_img.js';
import { PreloadImageEvent } from './events/image_preload.js';
import { HeaderMenuFormManager } from './tools/header_menu_form.js';


function viewTimeUTC() {
    const currentTime = new Date().toISOString().slice(0, 19).replace("T", " "); // Приводим время в формат "YYYY-MM-DD HH:MM:SS"
    const utcTime = document.getElementById("utc-time");
    utcTime ? utcTime.textContent = "UTC Time: " + currentTime : '';

}
function startTime() {
    viewTimeUTC();
    setInterval(viewTimeUTC, 1000);
}

// ====================================================================================== //


document.addEventListener('DOMContentLoaded', () => {
    console.log('\nAdmin Base Page script loaded Main.js ...');
    startTime();

    const apiClientJs = new RequestJs({baseUrl: window.location.origin + '/admin-api/'});
    const baseEv = new BaseEvent();
    baseEv.attachDOMEvents();
    
    // ----- //
    // Менеджер формы в хедере
    new HeaderMenuFormManager(baseEv);
    // Включаем оверлей для изображений
    enableImageOverlay();
    // Устанавливаем блок для отображения JSON данных
    setJSONBlocks( ['.initial-data-json'] );
    // Событие предпросмотра загружаемых изображений
    new PreloadImageEvent(baseEv);
    // События для полей выбора изображений с превью
    new SelectionEventsImage(baseEv, apiClientJs).init('select[id^="id_socials-"][id$="image"]');


    // ----- //
    document.body.classList.add("loaded");
    // Создаём и вызываем кастомное событие
    const event = new Event('baseLoaded');
    document.dispatchEvent(event);

});