'use strict';


class SubmittingForm {
    constructor(baseEv, apiClientJs) {
        this.baseEv = baseEv;
        this.apiClient = apiClientJs;

        this.init();
    }

    init() {
        this.baseEv.on('submit', '#submit-token-form', (ev, elm) => this.onSubmitForm(ev, elm));
    }

    checkError() {
        const el = document.querySelector('.error');
        if (!el) return;

        el.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });

        return true;
    }

    async onSubmitForm(ev, elm) {
        ev.preventDefault();
        if ( this.checkError() ) return;

        const formData = new FormData(elm);
        const resp = await this.apiClient.post( 'add-coin/', formData, { form: true } )

        console.log('Form Submission Response:', resp);

        if (resp.error) {
            const mainErrorElm = document.getElementById('main-error');
            mainErrorElm.textContent = resp.message ? resp.message : 'Error';
            mainErrorElm.className = 'error_1';
            setTimeout(() => location.reload(), 30000);
        } else {
            if (resp.redirect) {
                location = resp.redirect;
            } else {
                document.querySelector('.coin-success')?.classList.add('open');
            }
        }
    }
}


class FormEventManager {
    ERROR_CLASS = 'error';

    constructor(baseEv, apiClientJs) {
        this.baseEv = baseEv;
        this.apiClient = apiClientJs;

        this.dataForm = {
            name: '',
            symbol: '',
            contract_address: '',
            chain: '',
        }
        
        this.init();
    }
    
    init() {
        this.baseEv.on('change', '#token-name', (ev, elm) => this.onCheckNameSymbolField());
        this.baseEv.on('change', '#token-ticker', (ev, elm) => this.onCheckNameSymbolField());

        this.baseEv.on('change', '#contract-address, #token-chain', (ev, elm) => this.onCheckContractAddress());

        // Обработчик для полей социальных сетей
        const socials = [
            'website', 'twitter', 'telegram', 'discord', 'github',
            'medium', 'reddit', 'youtube', 'instagram',
            'linkedin', 'tiktok', 'whitepaper'
        ];
        socials.forEach( (s) => this.baseEv.on('change', `#${s}`, (ev, elm) => this.onCheckSocialField(ev, elm)) );
    }

    clearError() {
        document.querySelectorAll('.error').forEach( elm => elm.classList.remove('error') );
        const errorMessages = document.querySelectorAll('.error-wrapp-form span');
        errorMessages.forEach( elm => elm.textContent = '' );
    }

    setErrorMessage(data) {
        this.clearError();
        if ( data.success ) return;

        data.errors?.forEach(dataError => {
            const selectorMsgError = dataError.selectors_msg_error;
            const selectorsElmsError = dataError.selectors_elms_error;
            const errorMsg = dataError.error_msg;

            for ( const selector of selectorsElmsError ) {
                document.querySelectorAll(selector).forEach( elm => elm.classList.add(this.ERROR_CLASS) );
            }
            const elmErrorMsg = document.querySelector(selectorMsgError);
            elmErrorMsg.textContent = errorMsg;
        })
    }

    async checkDataForm() {
        const resps = await this.apiClient.post('check-data-form/', this.dataForm);
        console.log('Check Data Form Response:', resps);
        this.setErrorMessage(resps);
    }

    async onCheckNameSymbolField() {
        const nameCoin = document.getElementById('token-name').value.trim();
        const symbolCoin = document.getElementById('token-ticker').value.trim();

        if (nameCoin.length < 3 || symbolCoin.length < 3) {
            return;
        }

        this.dataForm.name = nameCoin;
        this.dataForm.symbol = symbolCoin;
        await this.checkDataForm();

    }

    async onCheckContractAddress() {
        const contract = document.getElementById('contract-address').value.trim();
        const chain = document.getElementById('token-chain').value.trim();
        console.log(`\nContract Address: ${contract}\nChain: ${chain}`);

        this.dataForm.contract_address = contract;
        this.dataForm.chain = chain;
        await this.checkDataForm();
    }

    // ----------------------------- //
    isValidURL(str) {
        try {
            const url = new URL(str);

            const isHttp = url.protocol === "http:" || url.protocol === "https:";

            // Проверка: в hostname есть хотя бы одна точка и домен верхнего уровня
            const hasDomain = /\.[a-z]{2,}$/i.test(url.hostname);

            return isHttp && hasDomain;
        } catch (_) {
            return false;
        }
    }

    normalizeURL(str) {
        str = str.trim();
        if (!str) return '';
        // Регулярное выражение для определения протокола
        const hasProtocol = /^(https?|ftp|file|ws|wss):\/\//i.test(str);
        // Если есть протокол, заменяем его на https://
        if (hasProtocol) {
            // Удаляем старый протокол и добавляем https://
            return 'https://' + str.replace(/^(https?|ftp|file|ws|wss):\/\//i, '');
        }
        // Если начинается с // (протокол-относительный URL), убираем //
        if (str.startsWith('//')) {
            return 'https://' + str.substring(2);
        }
        // В остальных случаях просто добавляем https://
        return 'https://' + str;
    }


    isValidTelegramURL(str) {
        return /^https:\/\/(www\.)?t\.me\/[a-zA-Z0-9_]{5,64}$/.test(str);
    }

    isValidTwitterURL(str) {
        return /^https:\/\/(www\.)?(x\.com|twitter\.com)\/([a-zA-Z0-9_]{1,15}(\/status\/[0-9]+)?|i\/(communities|lists)\/[0-9]+)$/.test(str);
    }


    isValidDiscordURL(str) {
        return /^https:\/\/(www\.)?discord\.gg\/[a-zA-Z0-9]+$/.test(str);
    }

    isValidTikTokURL(str) {
        return /^https:\/\/(www\.)?tiktok\.com\/@[\w.-]+$/.test(str);
    }

    isValidRedditURL(str) {
        return /^https:\/\/(www\.)?reddit\.com\/r\/[a-zA-Z0-9_]+\/?$/.test(str);
    }

    isValidInstagramURL(str) {
        return /^https:\/\/(www\.)?instagram\.com\/[a-zA-Z0-9_.]+\/?$/.test(str);
    }

    isValidYouTubeURL(str) {
        return /^https:\/\/(www\.)?youtube\.com\/(channel|c|user)\/[a-zA-Z0-9_-]+$/.test(str);
    }

    isValidFacebookURL(str) {
        return /^https:\/\/(www\.)?facebook\.com\/[a-zA-Z0-9.]+$/.test(str);
    }

    isValidMediumURL(str) {
        return /^https:\/\/(www\.)?medium\.com\/@?[a-zA-Z0-9_.-]+$/.test(str);
    }

    isValidGithubURL(str) {
        return /^https:\/\/(www\.)?github\.com\/[a-zA-Z0-9_.-]+$/.test(str);
    }


    onCheckSocialField(ev, elm) {
        const socialID = elm.id;
        const dataField = elm.value?.trim() || '';
        const normalized = this.normalizeURL(dataField);
        console.log("Normalized URL:", normalized);

        if ( normalized !== dataField ) elm.value = normalized;  // Приводим к формату https://...
        
        let isValid = false;
        switch (socialID) {
            case 'website':
            case 'whitepaper':
                isValid = this.isValidURL(normalized);
                break;
            case 'telegram':
                isValid = this.isValidTelegramURL(normalized);
                break;
            case 'twitter':
                isValid = this.isValidTwitterURL(normalized);
                break;
            case 'discord':
                isValid = this.isValidDiscordURL(normalized);
                break;
            case 'tiktok':
                isValid = this.isValidTikTokURL(normalized);
                break;
            case 'reddit':
                isValid = this.isValidRedditURL(normalized);
                break;
            case 'instagram':
                isValid = this.isValidInstagramURL(normalized);
                break;
            case 'youtube':
                isValid = this.isValidYouTubeURL(normalized);
                break;
            case 'facebook':
                isValid = this.isValidFacebookURL(normalized);
                break;
            case 'medium':
                isValid = this.isValidMediumURL(normalized);
                break;
            case 'github':
                isValid = this.isValidGithubURL(normalized);
                break;
        }

        const infoElementId = `error_${socialID}`;
        const infoElement = document.getElementById(infoElementId);

        if (!infoElement) return; // если элемента нет, выходим

        if (isValid || normalized.length === 0) {
            elm.classList.remove(this.ERROR_CLASS); // удаляем класс ошибки
            infoElement.textContent = '';
        } else {
            elm.classList.add(this.ERROR_CLASS); // добавляем класс ошибки
            infoElement.textContent = ' Invalid URL';
        }
    }

}


export function init_add_coin_page(baseEv, apiClientJs) {
    console.log('\nAdd Coin Page script loaded ...');

    new FormEventManager(baseEv,  apiClientJs);
    new SubmittingForm(baseEv, apiClientJs);
}

