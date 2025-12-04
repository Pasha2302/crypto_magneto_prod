'use strict';


export class BaseEvent {
    constructor() {
        this.events = new Map();
    }

    on(eventType, selectorOrCallback, callback) {
        let selector = null;
        if (typeof selectorOrCallback === 'string') {
            selector = selectorOrCallback;
        } else {
            callback = selectorOrCallback;
        }

        if (!this.events.has(eventType)) this.events.set(eventType, []);
        this.events.get(eventType).push({ selector, callback });
    }

    off(eventType, callback) {
        if (!this.events.has(eventType)) return;
        const listeners = this.events.get(eventType).filter(l => l.callback !== callback);
        this.events.set(eventType, listeners);
    }

    emit(eventType, event) {
        if (!this.events.has(eventType)) return;
        this.events.get(eventType).forEach(({ selector, callback }) => {
            // console.log("Event emitted:", eventType, event, selector, callback);
            if (!callback) return;

            let matchedEl = selector ? event.target.closest(selector) : event.target;
            if (matchedEl) {
                callback(event, matchedEl);
            }
        });
    }

    attachDOMEvents() {
        ['click', 'keydown', 'input', 'change', 'focusin', 'submit',].forEach(type => {
            document.addEventListener(type, e => this.emit(type, e));
        });
    }
}
