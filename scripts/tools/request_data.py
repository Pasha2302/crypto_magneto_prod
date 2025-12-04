from collections import namedtuple

RequestData = namedtuple(typename='RequestData', field_names=['url', 'cookies', 'headers', 'params'])

def get_rq_data_coin() -> RequestData:
    cookies = {
        '_ga': 'GA1.1.516450659.1760449246',
        '_csrf': 'MTc2MDQ5NjgyMnxJakJIYXk4eFFtMUthMmRuYVZKVE16UkhiRFJ2WlRkNWNtUkhMMWxRUmt0TGFtbDVUV0ZqUlRJeVpITTlJZ289fC7hx3TV4g5oTs9CuHlGblHZwdsTAbGofhgqqHPVvY2g',
        '_ga_133NR9785E': 'GS2.1.s1760496823$o2$g1$t1760525172$j60$l0$h1406179232',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://whale-alert.io/',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'alerts': '9',
        'prices': 'BTC',
        'hodl': 'bitcoin,BTC',
        'potential_profit': 'bitcoin,BTC',
        'average_buy_price': 'bitcoin,BTC',
        'realized_profit': 'bitcoin,BTC',
        'volume': 'bitcoin,BTC',
        # 'news': 'true',
        # 'news': 'false',
    }

    url = 'https://whale-alert.io/data.json'
    return RequestData(url=url, cookies=cookies, headers=headers, params=params)


def get_rq_data_graph():
    cookies = {
        '_ga': 'GA1.1.516450659.1760449246',
        '_csrf': 'MTc2MDQ5NjgyMnxJakJIYXk4eFFtMUthMmRuYVZKVE16UkhiRFJ2WlRkNWNtUkhMMWxRUmt0TGFtbDVUV0ZqUlRJeVpITTlJZ289fC7hx3TV4g5oTs9CuHlGblHZwdsTAbGofhgqqHPVvY2g',
        'a-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlB5dGhvbkZyZWVsYW5jZUB5YW5kZXgucnUiLCJleHAiOjE3NjMxMjQ2NjUsImlhdCI6MTc2MDUzMjY2NX0.KBnyVocz-COSYQpmKXLCtAcUiDDtwv7gl-lQkoN3xOU',
        '_ga_133NR9785E': 'GS2.1.s1760496823$o2$g1$t1760532926$j31$l0$h1406179232',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://whale-alert.io/',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'name': 'price',
        'duration': '1h',
        'blockchain': 'ethereum',
        'symbol': 'ETH',
    }

    url = 'https://whale-alert.io/graph.json'
    # url = 'https://whale-alert.io/graph-plan.json'
    return RequestData(url=url, cookies=cookies, headers=headers, params=params)
