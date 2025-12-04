'use strict';


export class PreloadImageEvent {
    constructor(baseEv) {
        this.baseEv = baseEv;

        this.init();
    }

    init() {
        this.baseEv.on('change', '', (e, elm) => this.onFileInput(e));
    }

    onFileInput(e) {
        const el = e.target;
        if (el.tagName !== 'INPUT' || el.type !== 'file') return;
        if (!el.files || !el.files[0]) return;

        const file = el.files[0];

        // Контейнер, где должен появляться блок превью
        const wrapper = el.parentElement;

        // Удаляем старый <p> превью, если есть
        const existingPreview = wrapper.querySelector('p.custom-file-preview');
        if (existingPreview) existingPreview.remove();

        // Создаём новый <p> с превью
        const p = document.createElement('p');
        p.className = 'custom-file-preview';

        const a = document.createElement('a');
        a.href = URL.createObjectURL(file);
        a.target = '_blank';

        const img = document.createElement('img');
        img.className = 'custom-img-form';
        img.src = a.href;
        img.alt = 'Image';

        a.appendChild(img);
        p.textContent = 'Current file: ';
        p.appendChild(a);

        wrapper.prepend(p);  // Добавляем превью в начало контейнера
    }

}

