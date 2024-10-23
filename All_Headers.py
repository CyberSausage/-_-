
main_headers = {
            "cookie": "ваши куки из SMMO",
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

photo_headers = {**{'Accept': 'image/png'}, **main_headers}

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Origin': 'https://web.simple-mmo.com',
    'Referer': 'https://web.simple-mmo.com/travel',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}

base_headers = {**header, **main_headers}