import requests

def dump_barbora_html():
    print("📥 Downloading Barbora HTML...")
    
    # ---> PASTE YOUR COOKIES AND HEADERS HERE <---
    cookies = {
    'CookieConsent': '{stamp:%27g9aBuqvdiAyUypxiWIHQim4xKwAn0x+WwswMPlBTQ4CNIYv1+ojrKw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1778787500118%2Cregion:%27ee%27}',
    'X-Session-ID': '28ce105f-eca7-4781-a91a-c8316429e998',
    'BN-Checkout-Test-Group': 'true',
    'ConstructorioID_session_id': '1',
    'ConstructorioID_client_id': 'a3dd6dd0-267a-44c6-8d35-0bec0db92f1c',
    'ConstructorioID_session': '{"sessionId":1,"lastTime":1778791115779}',
    'AWSALBTG': 'YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe',
    'AWSALBTGCORS': 'YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe',
    'AWSALB': 'jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    'AWSALBCORS': 'jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    }

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,et;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://barbora.ee/pakkumised?page=2',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': 'CookieConsent={stamp:%27g9aBuqvdiAyUypxiWIHQim4xKwAn0x+WwswMPlBTQ4CNIYv1+ojrKw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1778787500118%2Cregion:%27ee%27}; X-Session-ID=28ce105f-eca7-4781-a91a-c8316429e998; BN-Checkout-Test-Group=true; ConstructorioID_session_id=1; ConstructorioID_client_id=a3dd6dd0-267a-44c6-8d35-0bec0db92f1c; ConstructorioID_session={"sessionId":1,"lastTime":1778791115779}; AWSALBTG=YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe; AWSALBTGCORS=YcSb+a9FjRA6U7u7OU/2Kq9pkzc27Jjv7CmKiDQa0zk5lTgevPp4T0+HEPrv+xDIhqDPJbdZwe+V/smaZfp1/aAJX2CxmU0En47e/q0FQ1VdyFMV+oXJXpxbgnlOu6huwXoNjveqnvWV+8p1i+6g/H5YOXhNzv2yejBGbAv5eXMe; AWSALB=jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO; AWSALBCORS=jaizLFt8kIp90R6je0d6sTPKR//RJd9B8tsc5rcVrZGszx1YYrxrtk5SA58vZF0XLAP1pDIDYQ3KgedSTC5WB95k40bHPcnI4+/a18CsEevxA6YXfy/e08WrPPZO',
    }
    
    url = 'https://barbora.ee/pakkumised'
    
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        
        # Save the raw webpage to a file
        with open("barbora_raw.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print("✅ Saved! Open 'barbora_raw.html' in VS Code.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    dump_barbora_html()