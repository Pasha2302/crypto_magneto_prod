'use strict';


export class MobileMenu {
    constructor(eventBus) {
        this.modal = document.getElementById("submenu-nav");
        this.eventBus = eventBus;
        this.init();
    }

    init() {
        this.eventBus.on('click', '#mobile-menu-toggle', (e) => this.toggleModal(e));
    }

    toggleModal(e) {
        const toggleElm = e.target.closest('#mobile-menu-toggle');

        if (toggleElm && this.modal) {
            const isActive = toggleElm.classList.toggle('active');
            this.modal.classList.toggle('active');

            // Lock/unlock body scroll
            if (isActive) {
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'fixed';
                document.body.style.width = '100%';
            } else {
                document.body.style.overflow = '';
                document.body.style.position = '';
                document.body.style.width = '';
            }
        }
    }


}

