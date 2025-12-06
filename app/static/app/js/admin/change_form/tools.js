'use strict';


function showHideInlineBlocks() {
    // Функция для сворачивания/разворачивания инлайн-блоков:

    $(".js-inline-admin-formset.inline-group, .collaps-block").each(function () {
        let $targetBlock = $(this);
        // Найдем заголовок h2
        let $title = $targetBlock.find("h2");
        // Создадим обертку для содержимого
        let $wrapper = $("<div class='inline-form-wrapper'></div>");
        // Переместим все после h2 в обертку
        console.log("\nTarget Block Collaps:", $title);
        $title.nextAll().wrapAll($wrapper);
        // Создаем кнопку для сворачивания
        let $toggleBtn = $("<button type='button' class='inline-toggle'>Expand</button>");
        // Добавляем кнопку перед заголовком
        $title.prepend($toggleBtn); // Кнопка перед текстом заголовка

        // Обработчик клика на кнопку
        $toggleBtn.on("click", function () {
            const $formContent = $targetBlock.find('.inline-form-wrapper');
            let isHidden = $formContent.is(":hidden");

            if (isHidden) {
                $formContent.slideDown(); // Показываем
                $(this).text("Collapse");  // Меняем текст кнопки
            } else {
                $formContent.slideUp(); // Скрываем
                $(this).text("Expand"); // Меняем текст кнопки
            }
        });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    console.log('\nTools script Base change forms loaded.');
    showHideInlineBlocks();
    
});
