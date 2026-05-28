import requests

cookies = {
    '__uzma': '059f033d-1ada-4ae7-981a-b97586e7e32d',
    '__uzmb': '1778511887',
    '__uzme': '6047',
    '__ssds': '0',
    '__ssuzjsr0': 'a9be0cd8e',
    '__uzmaj0': 'b086fa18-584b-4a4b-ac8a-8d847f2cf062',
    '__uzmbj0': '1778511889',
    '__uzmlj0': 'mhpO6z7Sllc/eM19qnJKnNvG1g3Cz3O54sTXUmHm96k=',
    'XSRF-TOKEN': 'eyJpdiI6IlRvbGRSeVJFRWhERlBENkRleW1Ya2c9PSIsInZhbHVlIjoibXZjS1ROWGRWQzJ5YU9qU0VMVllKYlA5UVVtOHE1MDRwRTZYdFRoVWswWjN3c0dJbDI5Wm00LzZhZWZ2a3NyNGlnS2lYTU00ZE9sVkQ3eU1XcmlRRmVKRkUrY3kyQ2hZdHpoMjh0ckgzUHZWdmtDUnJIM1kzVHdiRzlrTkxVVWwiLCJtYWMiOiJmZjNhNDIwYTM5Njc1MDg5NDU1YTkxY2EzZGRkYzgxNmRiNTI2MWRkNmVjYjMwNWMxZDk1YTE5ZGY3NzVkZWNlIiwidGFnIjoiIn0%3D',
    '__uzmcj0': '906273163495',
    '__uzmdj0': '1778516421',
    '__uzmfj0': '7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893734531716-000393414f314abf9aa31',
    'uzmxj': '7f900061b45d65-ed4a-4ad9-8426-6cd1540844f81-17785118893734531716-9ea8e473157abd1d31',
    '__uzmd': '1778516421',
    '__uzmc': '3431560169186',
    'rimi_storefront_session': 'eyJpdiI6ImVjcTNjZ3gyY05kZ3hsM0wyVGRFMVE9PSIsInZhbHVlIjoibTVFNVVmcTdxWmJZS0ROSmVkaDc5YUxiV0o5Q0MrT2RQaHBiNTIxdUhFNHJMNDdLaldHR0NFS1FMSjhRam5OMEtONlBSQ3BrQUNKbTg3dG5nK0EvMWFrTTg0ZTBKV3dJTGxkZlViYXBmbEMvWVV5dXd2SWVrU1VRcU5DTlFydDEiLCJtYWMiOiI1Y2ViZDMwYjgzM2VlZTFjZDE0NmY4MGRjM2M2NzAxOGE0ZjczM2FjZDUwNjY5ZjUyNjg4NjNhY2E4ODgyZDBjIiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,et;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.rimi.ee/epood/ee/parimad-pakkumised?currentPage=1&pageSize=40',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'uzlc': '7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893734531716-000393414f314abf9aa3110016437467aluzmZb086fa18',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '__uzma=059f033d-1ada-4ae7-981a-b97586e7e32d; __uzmb=1778511887; __uzme=6047; __ssds=0; __ssuzjsr0=a9be0cd8e; __uzmaj0=b086fa18-584b-4a4b-ac8a-8d847f2cf062; __uzmbj0=1778511889; __uzmlj0=mhpO6z7Sllc/eM19qnJKnNvG1g3Cz3O54sTXUmHm96k=; XSRF-TOKEN=eyJpdiI6IlRvbGRSeVJFRWhERlBENkRleW1Ya2c9PSIsInZhbHVlIjoibXZjS1ROWGRWQzJ5YU9qU0VMVllKYlA5UVVtOHE1MDRwRTZYdFRoVWswWjN3c0dJbDI5Wm00LzZhZWZ2a3NyNGlnS2lYTU00ZE9sVkQ3eU1XcmlRRmVKRkUrY3kyQ2hZdHpoMjh0ckgzUHZWdmtDUnJIM1kzVHdiRzlrTkxVVWwiLCJtYWMiOiJmZjNhNDIwYTM5Njc1MDg5NDU1YTkxY2EzZGRkYzgxNmRiNTI2MWRkNmVjYjMwNWMxZDk1YTE5ZGY3NzVkZWNlIiwidGFnIjoiIn0%3D; __uzmcj0=906273163495; __uzmdj0=1778516421; __uzmfj0=7f9000b086fa18-584b-4a4b-ac8a-8d847f2cf0621-17785118893734531716-000393414f314abf9aa31; uzmxj=7f900061b45d65-ed4a-4ad9-8426-6cd1540844f81-17785118893734531716-9ea8e473157abd1d31; __uzmd=1778516421; __uzmc=3431560169186; rimi_storefront_session=eyJpdiI6ImVjcTNjZ3gyY05kZ3hsM0wyVGRFMVE9PSIsInZhbHVlIjoibTVFNVVmcTdxWmJZS0ROSmVkaDc5YUxiV0o5Q0MrT2RQaHBiNTIxdUhFNHJMNDdLaldHR0NFS1FMSjhRam5OMEtONlBSQ3BrQUNKbTg3dG5nK0EvMWFrTTg0ZTBKV3dJTGxkZlViYXBmbEMvWVV5dXd2SWVrU1VRcU5DTlFydDEiLCJtYWMiOiI1Y2ViZDMwYjgzM2VlZTFjZDE0NmY4MGRjM2M2NzAxOGE0ZjczM2FjZDUwNjY5ZjUyNjg4NjNhY2E4ODgyZDBjIiwidGFnIjoiIn0%3D',
}

params = {
    'query': '',
    'currentPage': '2',
    'pageSize': '40',
}

response = requests.get('https://www.rimi.ee/epood/ee/parimad-pakkumised', params=params, cookies=cookies, headers=headers)

data = response.json()
print(data['products'][:2000]) # Prints the first 2000 characters of the HTML