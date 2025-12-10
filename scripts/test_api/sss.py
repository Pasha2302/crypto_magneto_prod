import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.screenshotapi.net/',
    'Content-Type': 'application/json',
    'Origin': 'https://www.screenshotapi.net',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

json_data = {
    'url': 'coinmooner.com',
    'output': 'img',
    'file_type': 'png',
    'viewport': 'desktop',
    'blockCookiesBanner': False,
    'blockAds': False,
    'token': '0.8ECLCyaXjeXqMGmdXb_VCFVq6U4bGX5lfDsBIJOvBCATW_1RRzzr6SWb5H3qZ1tHZoV-jKlPSLr4YmtteZ2Yi9JGINzr5KLrYfJPdFe3Vfzq1N_XL9TE60y4S2GPKvLuTx4q9RXzX6OdOGbX020s1lHtNHJhV53Isqb838sGxZG3OVYS8WwinBii4L2eMCVfXISNDVUHNjMZPcmKynH-M9e6aZfH18AYOCPawBzfwfpXkSNCGhO-yLBhge4u6zxcKPhHLDiiPzL8f_oiyqyQVgwYu-_sYhsdg3NwA3W_QIxA6QFfh4x3BCpaxTB4Rf9BVx_8EStpzeI1u5gi7AgL22ddKmhJETgshPR2eEcVTsTldr6dojgamS3zteH09FCTw5QytBm8XiErm6f1XBkv8P1wMfR8VRJHPQz1ueQrHLtTZe6oUFjg-xtbYPxgI-ijo5ayEUrPzbCZlm_MOncSE3bNXVIsz95a9m4bXzOJO6eNQ1Kp6oDbDEMVXRdqJGUir18kHtNtabwmn31orBlHp7NbXnh6ASki5ZEu0s6yGVW0F3IBK0XEchpUYlos3rNTJKI_aItT1wYCFhUszKMf0EaOpNSJ7UVh4HAxtwEaoOHn_N_ivJGtYKAeiOrOlrUMZ7cILgGnWTWQ3FQYnCchnxT49oWIMl-cvUlEKIvgA3ccQoCCZ7oZQLciQjPuYqAb7OTYcv0kL4RMufmgRYSNCTv_Tnks9q3Wy1TT-CfpFon7md_KQf5-EtippXwgi6HS-jJTQIFkhS670IGsx8wwUugfTlKjTeJBSeP2DUFd1PFxTRGiCybD5KDigO2f-xtsCj-nVdRR1dnMfbOyuYsviHRRno-nvI7_BZGQexh-EV8.nNTKouA056ljCQCAUA7wwQ.79ceeab89c7cf19a6c893b129b91ba65b5052bc8d6957c82848a675b60866066',
}

response = requests.post('https://api.screenshotapi.net/v1/screenshot/try-screenshot', headers=headers, json=json_data)
print(response.content)