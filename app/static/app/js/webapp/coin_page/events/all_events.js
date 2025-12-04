'use strict';

export class AllEventsManager {
    constructor(baseEv) {
        this.baseEv = baseEv;
        
        this.init();
    }

    init() {
        this.baseEv.on('click', '.faq-question', (ev, elm) => this.toggleFaqAnswer(ev, elm));
        this.baseEv.on('click', '.copy-btn-header', (ev, elm) => this.copyContractAddress(ev, elm));
    }

    toggleFaqAnswer(ev, elm) {
        const parentBlock = elm.closest('.faq-item');
        if (!parentBlock) return;

        parentBlock.classList.toggle('active');
    }

    copyContractAddress(ev, elm) {
        const address = elm.dataset.address;
        if (!address) return;

        elm.style.background = 'rgb(17 255 19 / 51%)';

        navigator.clipboard.writeText(address).then(() => {
            const tooltip = elm.closest('.contract-detail').querySelector('.tooltip');
            if (tooltip) {
                tooltip.classList.add('show');
                setTimeout(() => {
                    tooltip.classList.remove('show');
                    elm.style.background = '';
                }, 1200);
            }
        }).catch(err => {
            console.error('Failed to copy address: ', err);
        });
    }
}