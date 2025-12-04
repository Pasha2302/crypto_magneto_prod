import json

import httpx   # uv add httpx


class RequestManager:
    def __init__(self, headers: dict, cookies: dict, is_proxy=False,):
        self.headers = headers
        self.cookies = cookies
        self.is_proxy = is_proxy
        self.client: httpx.Client | None = None

        self.proxy = None
        if is_proxy:
            self.proxy = "http://user130949:fduqey@159.148.253.16:8630"

    def get_json_data(self, url: str, params: dict) -> dict:
        response = httpx.get(url, params=params)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return {'error': 'Invalid JSON response', 'data': response.text, 'status_code': response.status_code}

    def get_page_html(self, url: str) -> str:
        response = self.client.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.text

    def set_client(self):
        self.client = httpx.Client(
                headers=self.headers,
                cookies=self.cookies,
                # params=self.params,
                timeout=40.0,
                verify=False,
                # Дополнительные настройки для HTTPS через прокси
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
                http1=True,  # Принудительно HTTP/1.1
                follow_redirects=True,  # Включить редиректы как в браузере
                proxy=self.proxy)

    def close(self):
        self.client.close()
        self.client = None

