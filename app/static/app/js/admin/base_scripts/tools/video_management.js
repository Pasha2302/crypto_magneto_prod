'use strict';


function initVideoOverlay() {
    const overlay = document.getElementById('video-overlay');
    const videoEl = document.getElementById('overlay-video');
    const closeBtn = document.getElementById('overlay-close');

    if (!overlay || !videoEl || !closeBtn) return;

    // Закрытие по кнопке
    closeBtn.addEventListener('click', () => {
        overlay.style.display = 'none';
        videoEl.pause();
        videoEl.src = '';
    });

    // Навешиваем на все мини-видео
    const miniVideos = document.querySelectorAll('.admin-video-thumb');
    miniVideos.forEach(video => {
        video.addEventListener('click', () => {
            showVideoOverlay(videoEl, overlay, video.dataset.src);
        });
    });

    // Навешиваем на все ссылки с видео в админке
    document.querySelectorAll("p.file-upload a").forEach(link => {
        const href = link.getAttribute("href") || "";

        // Проверяем что ссылка ведет на видеофайл
        if (href.match(/\.(mp4|webm|ogg)$/i)) {
            link.addEventListener("click", function (e) {
                e.preventDefault(); // запрещаем скачивание
                showVideoOverlay(videoEl, overlay, href);
            });
        }
    });
}


function showVideoOverlay(videoEl, overlay, src) {
    overlay.style.display = 'flex';

    videoEl.pause();
    // videoEl.muted = true;     // по умолчанию без звука
    videoEl.src = src;

    // Ждём загрузки метаданных
    videoEl.addEventListener('loadedmetadata', function handler() {
        console.log('Video metadata loaded, duration:', videoEl.duration);

        // Убираем слушатель, чтобы не сработал повторно
        videoEl.removeEventListener('loadedmetadata', handler);
        // Пытаемся запустить воспроизведение
        videoEl.play().catch(err => {
            console.warn('Video play was prevented:', err);
        });
        videoEl.volume = 0.05;     // 5% низкая громкость по умолчанию
        // setTimeout(() => {
        //     videoEl.currentTime = 60; // Перемотать на 60 секунд.
        // }, 5000);

    });
}


function videosPreviewOnHover() {
    // Навешиваем превью на все видео 

    document.querySelectorAll('.admin-video-thumb').forEach(video => {
        video.addEventListener('mouseenter', () => {
            video.currentTime = 10;
            video.play();
        });
        video.addEventListener('mouseleave', () => {
            video.pause();
            // video.currentTime = 0;
        });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    console.log('Admin [base_scripts] scripts Video Management loaded.');
    initVideoOverlay();
    // videosPreviewOnHover();   Сильно жрет оперативку !!
});