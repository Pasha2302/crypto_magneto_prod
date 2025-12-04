'use strict';


export class MainInputSearch {
    constructor(baseEv, apiClientJs) {
        this.baseEv = baseEv;
        this.apiClient = apiClientJs;

        this.searchToggle = document.getElementById('search-toggle');
        this.searchWrapperMobile = document.getElementById('header-search-wrapper');
        this.searchWrapperDesktop = document.querySelector('.header-search-desktop');

        this.searchClose = document.getElementById('search-close');
        this.searchInput = document.getElementById('search-input');

        this.dropdownMobile = document.getElementById('search-dropdown-mobile');
        this.dropdownDesktop = document.getElementById('search-dropdown-desktop');

        this.blockResultsMobile = document.getElementById('search-results-mobile');
        this.blockResultsDesktop = document.getElementById('search-results-desktop');

        this.CoinsData = [];

        this.init();
    }

    init() {
        // Обработка ввода в поле поиска
        this.baseEv.on( 'input', '#search-input', (e, elm) => this.inputData(e, elm, this.dropdownMobile, this.blockResultsMobile) );
        this.baseEv.on( 'input', '#search-input-desktop', (e, elm) => this.inputData(e, elm, this.dropdownDesktop, this.blockResultsDesktop) );

        this.baseEv.on('focusin', '#search-input-desktop', (e, elm) => this.inputFocus(e, elm, this.dropdownDesktop, this.blockResultsDesktop) );
        this.baseEv.on('focusin', '#search-input', (e, elm) => this.inputFocus(e, elm, this.dropdownMobile, this.blockResultsMobile) );

        // ------ //
        this.baseEv.on('click', '#search-toggle', (e) => this.showInput(e));
        this.baseEv.on('click', '#search-close', (e) => this.hideInput(e));
        

        // Закрытие по клику вне модальной формы.
        this.baseEv.on('click', '', (e) => {
            const target = e.target;
            const isCheck = (
                this.searchWrapperMobile.classList.contains('active') &&
                !this.searchWrapperMobile.contains(target) &&
                !this.searchToggle.contains(target)
            )
            if ( isCheck ) this.hideInput(e);

            if (this.searchWrapperDesktop && !this.searchWrapperDesktop.contains(target)) {
                this.dropdownDesktop.classList.remove('active');
            }
        });
        // Закрытие по нажатию Escape
        this.baseEv.on('keydown', (e) => {
            if (e.key === 'Escape') this.hideInput(e);
        });
    }

    addDataToResults(data, dropdown, resultsContainer) {
        // Render results
        if (data.length > 0) {
            resultsContainer.innerHTML = data.map(coin => `
        <a href="${coin.url}" class="search-result-item">
            <img 
                src="${ coin.img }" 
                class="chain-icon" 
                alt="${ coin.symbol }" 
                aria-label="${ coin.name }" >
            <div class="search-result-info">
            <div class="search-result-name">${coin.name}</div>
            </div>
            <div class="search-result-network">${coin.chain}</div>
        </a>
        `).join('');
            if (dropdown) dropdown.classList.add('active');
        } else {
            resultsContainer.innerHTML = '<div class="search-result-empty">No results found</div>';
            if (dropdown) dropdown.classList.add('active');
        }
    }

    performSearch(query, dropdown, resultsContainer, isFocus=false) {
        if (query.length === 0) {
            if (dropdown) dropdown.classList.remove('active');
            return;
        }

        if ( !isFocus ) {
            this.apiClient.post('search-coin/name/', { query: query }).then(data => {
                console.log("\nSearch API response:", data);
                this.dataCoins = data.coins || [];
                this.addDataToResults(this.dataCoins, dropdown, resultsContainer);
            }).catch(err => {
                console.error("Search API error:", err);
            });

        } else {
            this.addDataToResults(this.dataCoins, dropdown, resultsContainer);
        }
        
    }

    inputFocus(e, elm, dropdown, resultsContainer) {
        const trimmedQuery = elm.value ? elm.value.trim().toLowerCase() : '';
        this.performSearch(trimmedQuery, dropdown, resultsContainer, true);
    }

    inputData(e, elm, dropdown, resultsContainer) {
        const trimmedQuery = elm.value ? elm.value.trim().toLowerCase() : '';
        console.log("Search query:", trimmedQuery);
        this.performSearch(trimmedQuery, dropdown, resultsContainer);
    }

    // ------- ///

    showInput(e) {
        this.searchWrapperMobile.classList.add('active');
        // Фокусируйтесь на вводе поиска после небольшой задержки, чтобы разрешить анимацию
        setTimeout(() => {
            if (this.searchInput) this.searchInput.focus();
        }, 100);
    }

    hideInput(e) {
        this.searchWrapperMobile.classList.remove('active');
        if (this.searchInput) {
            this.searchInput.value = '';
            this.searchInput.blur();  // Убираем фокус с поля ввода

            this.dropdownDesktop.classList.remove('active');
            this.dropdownMobile.classList.remove('active');
            
            this.blockResultsDesktop.innerHTML = '';
            this.blockResultsMobile.innerHTML = '';
        }
    }

}
