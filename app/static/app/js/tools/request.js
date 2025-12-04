'use strict';


export class RequestJs {
    constructor(options = {}) {
        this.baseUrl = options.baseUrl || '';
        this.defaultHeaders = options.defaultHeaders || {
            'Accept': 'application/json'
        };
        this.timeout = options.timeout || 30000; // ms
    }

    // Попытка получить CSRF токен: из cookie или meta tag
    _getCsrfToken() {
        // По умолчанию Django ставит csrftoken в cookie
        const match = document.cookie.match(/(^|;)\\s*csrftoken=([^;]+)/);
        if (match) return decodeURIComponent(match[2]);
        // Альтернативно — meta tag
        const meta = document.querySelector('meta[name="csrf-token"], meta[name="csrfmiddlewaretoken"]');
        if (meta) return meta.getAttribute('content');

        return null;
    }

    _buildUrl(path, params) {
        const url = new URL(path, this.baseUrl || window.location.origin);
        if (params && typeof params === 'object') {
            Object.keys(params).forEach(key => {
                const val = params[key];
                if (val === undefined || val === null) return;
                if (Array.isArray(val)) {
                    val.forEach(v => url.searchParams.append(key, v));
                } else {
                    url.searchParams.append(key, val);
                }
            });
        }
        return url.toString();
    }

    /**
     * Выполняет fetch с автоматическим прерыванием по таймауту через AbortController.
     *
     * @async
     * @function _fetchWithTimeout
     * @param {RequestInfo} resource - URL или объект Request.
     * @param {RequestInit} [options={}] - Опции fetch; сюда будет добавлен signal для отмены.
     * @param {number} [timeoutMs] - Таймаут в миллисекундах. По умолчанию используется this.timeout.
     * @returns {Promise<Response>} Результат fetch, если запрос завершился до таймаута.
     * @throws {DOMException|Error} Бросает AbortError при таймауте или другие ошибки сети.
     *
     * Пример использования:
     * const res = await this._fetchWithTimeout('/api/data', { method: 'GET' }, 5000);
     *
     * Пояснение по AbortController (кратко):
     * - const controller = new AbortController(); создаёт объект контроллера отмены. У контроллера есть свойство `signal`.
     * - Этот `signal` передаётся в fetch через опцию { signal: controller.signal }, чтобы fetch мог быть отменён извне.
     * - setTimeout вызывает controller.abort() по истечении заданного таймаута, что приводит к отклонению fetch с ошибкой AbortError.
     * - AbortController — стандартный Web API для отмены асинхронных операций (fetch, потоки и т.п.).
     */
    async _fetchWithTimeout(resource, options = {}, timeoutMs) {
        // 
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeoutMs || this.timeout);
        try {
            const res = await fetch(resource, { ...options, signal: controller.signal });
            clearTimeout(id);
            return res;
        } catch (err) {
            clearTimeout(id);
            throw err;
        }
    }

    async request(path, opts = {}) {
        const method = (opts.method || 'GET').toUpperCase();
        const params = opts.params || null;
        const form = !!opts.form; // если true — ожидать FormData или не устанавливать Content-Type
        const timeout = opts.timeout || this.timeout;
        const credentials = opts.credentials || 'same-origin'; // для Django обычно same-origin

        const url = this._buildUrl(path, params);

        const headers = Object.assign({}, this.defaultHeaders, opts.headers || {});
        const isJsonBody = !form && opts.body && !(opts.body instanceof FormData);

        if (isJsonBody) {
            headers['Content-Type'] = headers['Content-Type'] || 'application/json';
        }

        // CSRF для небезопасных методов
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
            const csrf = this._getCsrfToken();
            if (csrf) headers['X-CSRFToken'] = csrf;
        }

        const fetchOpts = {
            method,
            headers,
            credentials
        };

        if (opts.body !== undefined && opts.body !== null) {
            fetchOpts.body = isJsonBody ? JSON.stringify(opts.body) : opts.body;
        }

        let response;
        try {
            response = await this._fetchWithTimeout(url, fetchOpts, timeout);
        } catch (err) {
            // Fetch/network error or abort (timeout)
            const isAbort = err.name === 'AbortError';
            const message = isAbort ? 'Request timed out' : (err.message || 'Network error');
            const error = new Error(message);
            error.type = isAbort ? 'timeout' : 'network';
            throw error;
        }

        const contentType = response.headers.get('Content-Type') || '';
        let data = null;

        // Попробовать распарсить JSON если можно
        if (response.status !== 204) {
            if (contentType.includes('application/json')) {
                try {
                    data = await response.json();
                } catch (e) {
                    data = null;
                }
            } else {
                data = await response.text();
            }
        }

        if (!response.ok) {
            const err = new Error('HTTP error: ' + response.status);
            err.status = response.status;
            err.data = data;
            throw err;
        }

        return data;
    }

    get(path, params, opts = {}) {
        return this.request(path, Object.assign({}, opts, { method: 'GET', params }));
    }

    post(path, body, opts = {}) {
        return this.request(path, Object.assign({}, opts, { method: 'POST', body, form: opts.form }));
    }

    put(path, body, opts = {}) {
        return this.request(path, Object.assign({}, opts, { method: 'PUT', body, form: opts.form }));
    }

    patch(path, body, opts = {}) {
        return this.request(path, Object.assign({}, opts, { method: 'PATCH', body, form: opts.form }));
    }

    delete(path, bodyOrParams, opts = {}) {
        // Поддерживаем вызов delete(path, params) и delete(path, body, {form:true})
        if (opts && opts.useParams) {
            return this.request(path, Object.assign({}, opts, { method: 'DELETE', params: bodyOrParams }));
        }
        return this.request(path, Object.assign({}, opts, { method: 'DELETE', body: bodyOrParams }));
    }

    setDefaultHeader(key, value) {
        this.defaultHeaders[key] = value;
    }

    removeDefaultHeader(key) {
        delete this.defaultHeaders[key];
    }
}


// ----------------------------------------------------------------------------------------- //

// Примеры использования класса RequestJs:
const funcExample = () => {
    const apiClient = new RequestJs({ baseUrl: window.location.origin + '/api/v1/' });

    // GET с параметрами (query)
    apiClient.get('items/', { page: 2, tags: ['btc', 'eth'] })
        .then(data => console.log('GET items', data))
        .catch(err => console.error('GET error', err));

    // POST JSON (async/await)
    (async () => {
        try {
            const newItem = { name: 'Alert', threshold: 50000 };
            const res = await apiClient.post('alerts/', newItem);
            console.log('Created alert', res);
        } catch (err) {
            console.error('POST error', err);
        }
    })();

    // Отправка FormData (файл) — не устанавливаем Content-Type вручную
    const fileInput = document.querySelector('#file-input');
    if (fileInput) {
        fileInput.addEventListener('change', async (e) => {
            const fd = new FormData();
            fd.append('file', e.target.files[0]);
            fd.append('description', 'Whale snapshot');

            try {
                const r = await apiClient.post('uploads/', fd, { form: true });
                console.log('Upload response', r);
            } catch (err) {
                console.error('Upload error', err);
            }
        });
    }

    // PUT / PATCH
    apiClient.put('alerts/123/', { threshold: 60000 })
        .then(data => console.log('Updated (PUT)', data))
        .catch(err => console.error('PUT error', err));

    apiClient.patch('alerts/123/', { active: false })
        .then(data => console.log('Updated (PATCH)', data))
        .catch(err => console.error('PATCH error', err));

    // DELETE используя query params (useParams)
    apiClient.delete('alerts/', { id: 123 }, { useParams: true })
        .then(data => console.log('Deleted via params', data))
        .catch(err => console.error('DELETE error', err));

    // Установка и удаление глобального заголовка
    apiClient.setDefaultHeader('X-App-Version', '1.2.3');
    // ...
    apiClient.removeDefaultHeader('X-App-Version');

    // Таймаут для одного запроса (ms) и обработка таймаута/сети
    apiClient.get('heavy/', null, { timeout: 5000 })
        .then(data => console.log('Heavy data', data))
        .catch(err => {
            if (err.type === 'timeout') {
                console.error('Request timed out');
            } else if (err.type === 'network') {
                console.error('Network error', err);
            } else {
                console.error('Request failed', err);
            }
        });

}
