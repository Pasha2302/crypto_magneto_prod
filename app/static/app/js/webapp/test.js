'use strict';


function setEventSwiperBlock() {
    // Получаем элемент с классом .swiper-track — это "лента", которая двигается
    const track = document.querySelector('.swiper-track');

    // Координаты и состояния
    let startX = 0;           // Позиция курсора/пальца в момент начала свайпа
    let currentTranslate = 0; // Текущее смещение ленты
    let prevTranslate = 0;    // Предыдущее смещение после последнего свайпа
    let isDragging = false;   // Флаг — сейчас двигаем или нет
    let diff = 0              // Сколько перетащили в px
    const threshold = 0.4;    // Порог (40% ширины слайда) для смены слайда

    // Навешиваем события для мыши
    track.addEventListener('mousedown', startDrag);
    track.addEventListener('mousemove', drag);
    track.addEventListener('mouseup', endDrag);
    track.addEventListener('mouseleave', endDrag);

    // Навешиваем события для сенсорных экранов
    track.addEventListener('touchstart', startDrag);
    track.addEventListener('touchmove', drag);
    track.addEventListener('touchend', endDrag);

    // Начало перетаскивания
    function startDrag(e) {
        console.log("\nMouse Event:", e.type);
        track.style.transition = 'none'; // Отключаем CSS-плавность при перетаскивании
        isDragging = true;               // Включаем флаг перетаскивания
        startX = getPositionX(e);        // Запоминаем стартовую координату X
    }

    // Перетаскивание
    function drag(e) {
        if (!isDragging) return;

        const currentX = getPositionX(e);       // Текущая координата
        diff = currentX - startX;         // Сдвиг относительно старта
        currentTranslate = prevTranslate + diff;  // Добавляем сдвиг к предыдущему положению
        track.style.transform = `translateX(${currentTranslate}px)`; // Мгновенное движение за курсором
    }

    // Конец перетаскивания
    function endDrag() {
        if (!isDragging) return;
        isDragging = false;               // Выключаем флаг
        track.style.transition = '';      // Возвращаем плавность из CSS
        const testCurrentTranslate = currentTranslate;
        const slideWidth = track.querySelector('.swiper-slide').offsetWidth; // Ширина одного слайда

        let movedSlides;
        // Логика порога зависит от направления движения
        // Math.round(x) — округляет число x до ближайшего целого
        let currentMovedSlides = -currentTranslate / slideWidth;
        currentMovedSlides = diff > 0 ? currentMovedSlides - threshold : currentMovedSlides + threshold
        movedSlides = Math.round(currentMovedSlides);


        const maxIndex = track.children.length - 1;             // Индекс последнего слайда
        const index = Math.min(Math.max(movedSlides, 0), maxIndex); // Ограничиваем диапазон

        // Вычисляем новое положение ленты
        currentTranslate = -index * slideWidth;
        prevTranslate = currentTranslate;

        // Перемещаем ленту к нужному слайду с плавной анимацией из CSS
        track.style.transform = `translateX(${currentTranslate}px)`;

        console.log(
`
diff: ${diff}
Slide Width: ${slideWidth}
Current Translate: ${testCurrentTranslate} (-) ${-testCurrentTranslate}

currentMovedSlides -currentTranslate / slideWidth : ${currentMovedSlides}
Moved Slides Math.round(currentMovedSlides + 0.3) : ${movedSlides}

Max Index (track.children.length - 1) ${maxIndex}
Index (Math.min(Math.max(movedSlides, 0), maxIndex)):  ${index}

Вычисляем новое положение ленты:
    Current Translate (-index * slideWidth) : ${currentTranslate} 
`
        )

    }

    // Универсальная функция получения X (мышь или тач)
    function getPositionX(e) {
        return e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
    }
}


// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log("Test JS loaded");
    setEventSwiperBlock();
});

// Math.round(x)  — округляет число x до ближайшего целого
//    0.3 → 0
//    0.5 → 1
//    0.7 → 1
//
// Math.floor(x)  — округляет число x **вниз** (к меньшему целому)
//    0.3 → 0
//    0.7 → 0
//    -0.3 → -1
//
// Math.ceil(x)   — округляет число x **вверх** (к большему целому)
//    0.3 → 1
//    0.7 → 1
//    -0.3 → 0
