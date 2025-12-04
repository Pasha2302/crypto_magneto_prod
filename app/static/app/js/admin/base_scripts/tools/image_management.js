'use strict';


export function enableImageOverlay(selector = "img") {
    // создаём элементы один раз
    const overlay = document.createElement("div");
    overlay.className = "image-overlay";
    overlay.style.display = "none";

    overlay.innerHTML = `
        <div class="image-overlay-content">
            <button class="overlay-close" aria-label="Закрыть">&times;</button>
            <img class="overlay-img" src="" alt="preview">
        </div>
    `;
    document.body.appendChild(overlay);

    const imgEl = overlay.querySelector(".overlay-img");
    const closeBtn = overlay.querySelector(".overlay-close");
    const content = overlay.querySelector(".image-overlay-content");

    // показать
    // document.addEventListener("mouseenter", e => {
    document.addEventListener("click", e => {
        if (e.target.matches(selector)) {
            const src = e.target.dataset.largeSrc || e.target.src;
            // Проверяем, что это не svg
            if (src.toLowerCase().endsWith(".svg")) return;
            imgEl.src = src;
            overlay.style.display = "flex";
        }
    }, true);

    // закрыть по крестику
    closeBtn.addEventListener("click", () => {
        overlay.style.display = "none";
        imgEl.src = "";
    });

    // закрыть по Esc
    document.addEventListener("keydown", e => {
        if (e.key === "Escape" && overlay.style.display === "flex") {
            overlay.style.display = "none";
            imgEl.src = "";
        }
    });

    // закрыть по клику вне блока
    overlay.addEventListener("click", e => {
        if (!content.contains(e.target)) {
            overlay.style.display = "none";
            imgEl.src = "";
        }
    });

    // закрыть при уходе курсора с оверлея
    // document.querySelector('.image-overlay-content').addEventListener("mouseleave", () => {
    //     overlay.style.display = "none";
    //     imgEl.src = "";
    // });
}

