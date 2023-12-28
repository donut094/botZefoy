from os import get_terminal_size, system as sys, name as os_name
from re import findall
from io import BytesIO
from time import sleep
from base64 import b64decode, b64encode
from random import choices, choice, uniform
from string import ascii_letters, digits
from requests import post, get, Session
from datetime import datetime
from urllib.parse import unquote
from threading import Thread
from fake_useragent import UserAgent



class Zefoy:
    def __init__(self) -> None:
        self.banner = ['','','  ___    _  _   _  _____  ___    _____  _   _  _   _  _____ ',' (  _ \ (_)( ) ( )(  _  )(  _ \ (  _  )( ) ( )( ) ( )(_   _)','| | ) || ||  \| || ( ) || | ) || ( ) ||  \| || | | |/|| |','| | | )| ||     || | | || | | )| | | ||     || | | |_)| |',' | |_) || || | \ || (_) || |_) || (_) || | \ || (_) |  | |  ',' (____/ (_)(() (_)(_____)(____/ (_____)(() (_)(_____)  ( ) ','           (_)                         (_)             /(  ','                                                      (__)  ','BY : discord.gg/BATtTTYPYv']

        self.config = {
            'mode'  : None,
            'size': get_terminal_size().columns,
            'url'   : None, 
            'video_url': None
            }

        self.keys = {
            'key_1': None,
            'key_2': None,
            'id'   : None  
        }

        self.endpoints: dict[str] = {}
        self.threads: list[Thread] = []

    def title(self, content: str) -> None:
        sys(f'title {content}' if os_name == 'nt' else '')

    def clear(self) -> None:
        sys('cls' if os_name == 'nt' else 'clear')
        
    def hide_cursor(self) -> None:
        print('\033[?25l', end='')

    def title_info(self, video_id: str) -> None:
        headers = {
            'host': 'tikstats.io',
            'user-agent': UserAgent().chrome,
        }
        while True:
            try: 
                res = get(f'https://tikstats.io/video/{video_id}', headers=headers)
                input(findall(r'.innerText = "(.*)"', res))
                if res.status_code == 200:
                    self.title(f'Tiktok Bot ~ [Views: {res.json()["viewCount"]} Shares: {res.json()["shareCount"]} Likes: {res.json()["likeCount"]}]')
            except: 
                continue

            sleep(1)
        
    def _print(self, thing: str, content: str, new_line: bool = False, input: bool = False) -> None or str:
        
        self.hide_cursor()
        
        col = "\033[38;2;225;-;255m"
        first_part = f"[{thing}] | [{datetime.now().strftime('%H:%M:%S')}] {content}"
        new_part = ""
        
        counter = 0
        for caracter in first_part:
            new_part += col.replace('-', str(225 - counter * int(255/len(first_part)))) + caracter
            counter += 1 
            
        if input:
            return f"{new_part}"
            
        if not new_line:
            print(f"{new_part}{' '*(self.config['size'] - len(first_part))}\033[38;2;255;255;255m", end="\r")

        else:
            print(f"{new_part}{' '*(self.config['size'] - len(first_part))}\033[38;2;255;255;255m")
            
    def display(self, banner_to_display: list) -> str:
        
        color = "\033[38;2;225;-;255m"
            
        new_banner = ""
        counter = 0
        for line in self.banner:
            new_banner += color.replace('-', str(counter * int(255 / len(banner_to_display)))) + ' ' * int((self.config['size'] - len(line))/2) + line + "\033[38;2;255;255;255m\n"
            counter += 1

        return new_banner


    def wait(self, time: int) -> None:
        for time_spent in range(time):
            sleep(1)
            self._print('/', f'Remaining Time: {time - (time_spent + 1)}')
            
        self._print('!', f'Sending {self.config["mode"]}')

    def decode(self, text: str) -> str: # from tekky
        return b64decode(unquote(text[::-1])).decode()

    def get_id(self, url: str) -> str:
        try: self.keys['id'] =  int(findall(r'/video/(.*)', url)[0])
        except: self.keys['id'] =  int(str(findall(r'/video/(.*)', url)[0]).split('?')[0])

        thread = Thread(target=self.title_info, args= (str(self.keys['id']),),  name="title_info")
        thread.start()
        self.threads.append(thread)
        
        
    def keep_thread_alive(self) -> None:
        
        dict_args = {
            'title_info' : (str(self.keys['id']),),
            'get_id': self.config['video_url']
        }
        
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
                    new_thread = Thread(target= eval(thread.name), args=(dict_args[thread.name],), name= thread.name); new_thread.start()
                    self.threads.append(new_thread)
                                
    def solve(self, session: Session) -> None:
        input_choice = {}

        solved = False  

        while not solved:
            source_code = str(session.get('https://zefoy.com').text).replace('&amp;', '&')
            captcha_token = findall(r'<input type="hidden" name="(.*)">', source_code)

            if 'token' in captcha_token:
                captcha_token.remove('token')
                
            try:
                captcha_url    = findall(r'img src="([^"]*)"', source_code)[0]
            except:
                input(self._print('!', 'Zefoy may have blocked you or you have a vpn/adblock enabled', input=True))
                exit()

            token_answer = findall(r'type="text" name="(.*)" oninput="this.value', source_code)[0]
            encoded_image = b64encode(BytesIO(session.get('https://zefoy.com' + captcha_url).content).read()).decode('utf-8')
            captcha_answer = post(f"https://platipus9999.pythonanywhere.com/", json={'image': encoded_image}).text
            
            sleep(uniform(1, 2))

            data = {
                token_answer: captcha_answer,
            }

            for values in captcha_token:
                token, value = values.split('" value="')
                data[token] = value
            else:
                data['token'] = ''

            response = session.post('https://zefoy.com', data = data).text
            try:
                self.keys['key_1'] = findall(r'remove-spaces" name="(.*)" placeholder', response)[0]
                
                all_endpoints = findall(r'<h5 class="card-title mb-3"> (.*)</h5>\n<form action="(.*)">', response)
                valid_endpoints = findall(r'<button class="btn btn-primary rounded-0 t-(.*)-button">', response)
                
                if 'chearts' in valid_endpoints:
                    valid_endpoints[valid_endpoints.index('chearts')] = 'comments hearts'
                
                if not self.config['mode']:
                    counter = 0
                    print('')
                    for key, value in all_endpoints:
                        if 'Live' in key: key = 'Livestream'
                        if key.lower() in valid_endpoints:
                            counter += 1
                            self._print(f'{counter}', key.title(), True)
                            self.endpoints[key.title()] = value
                            input_choice[counter] = key
                    
                    self.config['mode'] = input_choice[int(input("\n" + self._print('?', 'Choice Your Method > ', input= True)))]
                
                solved = True
                self.clear()
                self._print('!', f'Captcha Solved as {captcha_answer}', True)
                
            except:
                continue

    def search(self, session: Session, remaining_time: bool or int = False) -> str:

        dict_res = {
            'Too many requests': "self._print('!','Too many requests'):self.wait(int(findall(r'var ltm=(.*);', response)[0]))",
            'Please try again later. Server too busy.': "input(self._print('/', 'Server Too Busy Try Later', input= True))",
            'Checking Timer...': "self.wait(int(findall(r'ltm=(.*);', response)[0]))"
        }

        if not remaining_time:
            rand_token = ''.join(choices(ascii_letters + digits, k=16))
            data = f'------WebKitFormBoundary{rand_token}\r\nContent-Disposition: form-data; name="{self.keys["key_1"]}"\r\n\r\n{self.config["video_url"]}\r\n------WebKitFormBoundary{rand_token}--\r\n'
            headers = {
                'authority': 'zefoy.com',
                'accept': '*/*',
                'accept-language': 'fr-FR,fr;q=0.8',
                'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary{}'.format(rand_token),
                'host': 'zefoy.com',
                'origin': 'https://zefoy.com',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': UserAgent().chrome,
                'x-requested-with': 'XMLHttpRequest',
            }

            sleep(1)
            response = self.decode(session.post(f'https://zefoy.com/{self.endpoints[self.config["mode"]]}', headers= headers, data= data).text)
            try:
                self.keys['key_2'] = findall(r'<input type="hidden" name="(.*)">', response)[0].split('" value="')[0]
            except:

                if 'Session expired' in response:
                    self._print('!', 'Session expired')
                    raise Exception
                
                for expected_response, to_do in dict_res.items():
                    if expected_response in response:
                        for thing in to_do.split(':'):
                            eval(thing)

        else:
            raise Exception
        
        
        sleep(uniform(1, 2)) 
        self.send(session)

    def send(self, session: Session) -> None:
        rand_token = ''.join(choices(ascii_letters + digits, k=16))
        data  = f'------WebKitFormBoundary{rand_token}\r\nContent-Disposition: form-data; name="{self.keys["key_2"]}"\r\n\r\n{self.keys["id"]}\r\n------WebKitFormBoundary{rand_token}--\r\n'

        headers = {
            'authority': 'zefoy.com',
            'accept': '*/*',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{rand_token}',
            'origin': 'https://zefoy.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': UserAgent().chrome,
            'x-requested-with': 'XMLHttpRequest'
            }
        
        sleep(uniform(1, 2))     
        response = self.decode(session.post('https://zefoy.com/{}'.format(self.endpoints[self.config['mode']]), headers= headers, data= data).text)
        
        if 'Successfully' and 'sent' in response:
            self._print("!", f"{self.config['mode']} Sent", True)

        elif 'Session expired' in response:
            self._print('!', 'Session expired')
            sleep(2)
            raise Exception

        else:
            try:
                remaining_time = int(findall(r'var ltm=(.*);', response)[0])
                self.search(session, remaining_time)
            except:
                self.search(session)
                
    def repeat_task(self, session: Session) -> None:
        self.solve(session)
        sleep(1)
        while True: 
            try: self.search(session)
            except: break    

    def start(self) -> None:  
        self.title(f'Tiktok Bot Zefoy.com [By : DinoDonut]') 
    
        self.clear()
        print(self.display(self.banner))
        
        self.config['video_url'] = input(self._print('?', "Video Url > ", input = True))
        
        Thread(target=self.get_id, args=(self.config['video_url'],),  name="get_id").start()
        
        while True:
            with  Session() as sess:
                sess.headers = {        
                    'authority'             : 'zefoy.com',
                    'origin'                : 'https://zefoy.com',
                    'authority'             : 'zefoy.com',
                    'cp-extension-installed': 'Yes',
                    'user-agent'            : UserAgent().chrome,
                    }
                self.repeat_task(sess)



if __name__ == '__main__':
    Zefoy().start()
