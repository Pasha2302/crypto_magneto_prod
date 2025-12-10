'use strict';


// export class TableFilterStateManager {
//     constructor(storageKey = 'table_filter_state') {
//         this.storageKey = storageKey;

//         this.defaultState = {
//             sort_field: "price",
//             sort_direction: "desc",
//             filter_options: {
//                 new: false,
//                 presale: false,
//                 doxxed: false,
//                 audited: false,
//             },
//             page_num: 1,
//             per_page: 10,
//             chain_symbol: null,
//             promoted_only: null,
//         };

//         this.state = this._loadState();
//         this.reset();
//     }

//     _saveState(state) {
//         localStorage.setItem(this.storageKey, JSON.stringify(state));
//     }

//     _loadState() {
//         const raw = localStorage.getItem(this.storageKey);
//         if (!raw) {
//             this._saveState(this.defaultState);
//             return structuredClone(this.defaultState);
//         }

//         try {
//             const parsed = JSON.parse(raw);
//             return { ...this.defaultState, ...parsed };
//         } catch {
//             this._saveState(this.defaultState);
//             return structuredClone(this.defaultState);
//         }
//     }

//     getState() {
//         return structuredClone(this.state);
//     }

//     getValue(path) {
//         let value = '';
//         const keys = path.split('.'); // например "filter_options.presale"
//         let obj = this.state;
//         while (keys.length > 1) {
//             obj = obj[keys.shift()];
//         }
//         value = obj[keys[0]];
//         return value;
//     } 

//     update(path, value) {
//         const keys = path.split('.'); // например "filter_options.presale"
//         let obj = this.state;

//         while (keys.length > 1) {
//             obj = obj[keys.shift()];
//         }
//         obj[keys[0]] = value;

//         this._saveState(this.state);
//     }

//     reset() {
//         this.state = structuredClone(this.defaultState);
//         this._saveState(this.state);
//     }
// }


export class TableFilterStateManager {
    constructor(storageKey = 'table_filter_state') {
        this.storageKey = storageKey; // формально больше не нужен, но оставляем для совместимости

        this.defaultState = {
            sort_field: "price",
            sort_direction: "desc",
            filter_options: {
                new: false,
                presale: false,
                doxxed: false,
                audited: false,
            },
            page_num: 1,
            per_page: 10,
            chain_slug: null,
            promoted_only: null,
        };

        this.state = this._loadState();
    }

    // Заглушка вместо сохранения
    _saveState(state) {
        // Ничего не делаем — состояние теперь только в оперативной памяти
    }

    // Создание состояния только из defaultState
    _loadState() {
        const filterPage = document.querySelector('.filters-container').dataset.filterpage;
        console.log('Filter Page from DOM:', filterPage);
        if (filterPage) {
            this.defaultState.filter_options[filterPage] = true;
        }
        return structuredClone(this.defaultState);
    }

    getState() {
        return structuredClone(this.state);
    }

    getValue(path) {
        const keys = path.split('.');
        let obj = this.state;
        while (keys.length > 1) {
            obj = obj[keys.shift()];
        }
        return obj[keys[0]];
    }

    update(path, value) {
        const keys = path.split('.');
        let obj = this.state;

        while (keys.length > 1) {
            obj = obj[keys.shift()];
        }

        obj[keys[0]] = value;

        this._saveState(this.state); // фактически ничего не делает
    }

    reset() {
        const per_page = this.state.per_page; // сохраняем per_page
        this.state = structuredClone(this.defaultState);
        this.state.per_page = per_page; // восстанавливаем per_page
        this._saveState(this.state); // ничего не делает
    }
}


export class TableFilterEventManager {

    constructor(baseEv, apiClientJs) {
        this.baseEv = baseEv;
        this.apiClient = apiClientJs

        this.wrappTableElm = document.getElementById('table-main-block');
        this.wrappTablePromotedElm = document.getElementById('table-promoted-block')
        
        this.stateManager = new TableFilterStateManager(); // <=== подключили менеджер состояния фильтров.

        this.init();
    }

    init() {
        this.baseEv.on( 'click', '.pagination-btn', (ev, elm) => this.onPagination(ev, elm) );
        this.baseEv.on( 'change', '.rows-selector', (ev, elm) => this.onPerPage(ev, elm) );

        this.baseEv.on( 'click', '#table-promoted-block .sortable', (ev, elm) => this.onSorting(ev, elm, true) );
        this.baseEv.on( 'click', '#table-main-block .sortable', (ev, elm) => this.onSorting(ev, elm) );
        this.baseEv.on( 'click', '.filters-container .filter-btn', (ev, elm) => this.onFilterBtn(ev, elm) );

        this.baseEv.on( 'change', '.filter-btn.filter-select', (ev, elm) => this.onSelectChain(ev, elm) );
        
    }

    async getDataTable(wrappTableElm, promFilter=null) {
        try {
            const dataFilter = this.stateManager.getState();
            const res = await this.apiClient.post(
                'coin-table/filter-view/',
                promFilter ? promFilter : dataFilter
            );

            if (res.html) wrappTableElm.innerHTML = res.html;

        } catch (err) {
            console.error('Request error', err);
        }
    }

    async onPagination(ev, elm) {
        const page_num = elm.dataset.page;
        if (!page_num) return;

        this.stateManager.update('page_num', Number(page_num));
        try {
            await this.getDataTable(this.wrappTableElm);
        
        } catch (err) { console.error('[onPagination] Request error', err) };
    }


    async onPerPage(ev, elm) {
        const per_page = elm.value.trim();
        // console.log("Per Page Value:", per_page);

        if (per_page) {
            this.stateManager.update( 'per_page', Number(per_page) );
            document.querySelectorAll('.rows-selector').forEach( elm => elm.value = per_page )
            this.getDataTable(this.wrappTableElm).catch( (err) => console.error('[onPerPage] Request error', err) );
        };
        
    }

    async onSelectChain(ev, elm) {
        const chain_slug = elm.value.trim();
        console.log("Selected Chain Slug:", chain_slug);

        this.stateManager.update( 'chain_slug', chain_slug ? chain_slug : null );
        this.getDataTable(this.wrappTableElm).catch( (err) => console.error('[onSelectChain] Request error', err) );
    }

    onSorting(ev, elm, promoted_only=null) {
        const sort_field = elm.dataset.column.trim().toLowerCase();
        let sort_direction = elm.dataset.sortDirection.trim().toLowerCase();

        switch (sort_direction) {
            case 'none':
                sort_direction = 'desc';
                break;
            case 'asc':
                sort_direction = 'desc';
                break;
            case 'desc':
                sort_direction = 'asc';
                break;
            default:
                sort_direction = 'desc';
        }
        console.log(`\nSort Field: ${sort_field}\nSort Direction: ${sort_direction}`);
        
        if (sort_direction && sort_field) {
            if ( promoted_only ) {
                this.getDataTable(
                    this.wrappTablePromotedElm,
                    {'promoted_only': promoted_only, 'sort_field': sort_field, 'sort_direction': sort_direction}
                ).catch( (err) => console.error('Request error', err) );

            } else {
                this.stateManager.update( 'sort_field', sort_field );
                this.stateManager.update( 'sort_direction', sort_direction );
                this.getDataTable(this.wrappTableElm).catch( (err) => console.error('[onSorting] Request error', err) );
            }
            
        };
    }

    onFilterBtn(ev, elm) {
        const filterOptions = elm.dataset.name ? elm.dataset.name.trim(): false;

        if ( filterOptions ) {
            if ( filterOptions === 'reset' ) {
                this.stateManager.reset();
                this.getDataTable(this.wrappTableElm).catch( (err) => console.error('[onFilterBtn] Request error', err) );
                document.querySelectorAll('.filters-container .filter-btn').forEach( elm => elm.classList.remove('filter-active') );
                document.querySelector('.filter-btn.filter-select').value = '';
                return;
            }

            const key = `filter_options.${filterOptions}`;
            let value = this.stateManager.getValue(key);
            console.log("Current Value:", value);
            value = value == false;
            console.log(`Filter Option Name: ${filterOptions}\nFilter Value: ${value}`);

            this.stateManager.update( key, value );
            // Смена активного класса:
            elm.classList.toggle('filter-active');
            this.getDataTable(this.wrappTableElm).catch( (err) => console.error('[onFilterBtn] Request error', err) );
        }

    }

}