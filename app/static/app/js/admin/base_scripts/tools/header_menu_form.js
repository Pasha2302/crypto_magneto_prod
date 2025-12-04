'use strict';


export class HeaderMenuFormManager {
    constructor(baseEv) {
        this.baseEv = baseEv;
        this.menuBlock = document.querySelector('.form-container__wrapp');

        if ( document.querySelector('#branding') ) {
            this.init()
        };
    }

    init() {
        // Устанавливаем фоновое изображение хедера, если задано:
        this.setBackgroundColorHeader();
        // Клик по бургеру
        this.baseEv.on('click', '.header__burger', (e, elm) => this.onBurgerMenu(e, elm));
    }

    setBackgroundColorHeader() {
        if (!headerImgPath) return;
        const block = document.getElementById("branding");
        block.style.backgroundImage = `url(${headerImgPath})`;
        block.style.backgroundSize = "cover";   // картинка по размеру блока
        block.style.backgroundPosition = "center"; // по центру
    }

    onBurgerMenu(e, elm) {
        const burger = elm;
        const menu = this.menuBlock;
    
        function closeMenu(b, m) {
            b.classList.remove('active');
            m.classList.remove('active');
            b.setAttribute('aria-expanded', 'false');
            m.setAttribute('aria-hidden', 'true');
        }
    
        function openMenu(b, m) {
            b.classList.add('active');
            m.classList.add('active');
            b.setAttribute('aria-expanded', 'true');
            m.setAttribute('aria-hidden', 'false');
        }
    
        const isOpen = burger.classList.toggle('active');
        if (isOpen) openMenu(burger, menu); else closeMenu(burger, menu);
    }
}
