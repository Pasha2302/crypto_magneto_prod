'use strict';


export class SelectionEventsImage {
    constructor(baseEv, apiClient) {
        this.baseEv = baseEv;
        this.apiClient = apiClient;

        this.imageMap = {};
    }

    init(selectors) {
        // Загружаем данные изображений с сервера:
        this.getDataImage(selectors);
        // Навешиваем обработчик изменения селектов:
        this.baseEv.on('change', selectors, (e, elm) => this.showImagePreview(e, elm));
    }

    async getDataImage(selectors) {
        const resp = await this.apiClient.get('get-image-social/');
        console.log('getDataImage response:', resp);
        if (resp && resp.data) {
            this.imageMap = resp.data;
            // Инициализируем превью для всех селектов при загрузке страницы:
            document.querySelectorAll(selectors).forEach(elm => this.showImagePreview(null, elm));
        }
    }

    createImgPreview(target) {
        // <img src="" class="label-image-preview" style="width: 30px; height: 30px;" />
        // <div class="image-wrapper"></div>
        const wrapper = document.createElement('div');
        wrapper.classList.add('img-preview-wrapper');
        target.insertAdjacentElement('beforebegin', wrapper);

        const img = document.createElement('img');
        img.classList.add('label-image-preview');
        img.style.width = '30px';
        img.style.height = '30px';
        // Вставляем после селекта:
        // target.insertAdjacentElement('afterend', img);
        // Вставляем перед селектом:
        // target.insertAdjacentElement('beforebegin', img);
        wrapper.appendChild(img);
        return img;
    }

    showImagePreview(e, elm) {
        if (!elm || elm.tagName !== 'SELECT') return;
        const value = elm.value;
        const parentBlock = elm.parentElement;
        let imgPreview = parentBlock.querySelector('.label-image-preview');
        if (!imgPreview) imgPreview = this.createImgPreview(elm);

        if (!value) {
            imgPreview.closest('.img-preview-wrapper')?.remove();
            return;
        }

        const imgUrl = this.imageMap[Number(value)] || '';
        imgPreview.src = imgUrl;
    }
}
