import requests, time
from bs4 import BeautifulSoup
import random

class Amazon:
    def __init__(self):
        self.headers = (
            {
                'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': self.header(),
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.amazon.com/',
                'accept-language': 'es-ES',
            }
        )
        self.wait = []
    
    def header(self):
        agents_list = [x for x in open('agents', 'r').readlines()]
        ran = random.choice(agents_list)
        return(str(ran.strip()))

    
    def build_urls(self):
        asins_file = open('asins', 'r')
        urls = [ parse(x) for x in asins_file.readlines()]
        # URL = "https://www.amazon.com/-/es/dp/B01H6GUCCQ"
        return urls
        
    def build_url(self, data):
        url = parse(data)
        return url
    
    def proxy(self):
        proxy = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps').json()
        proxy = random.choice(proxy['data'])
        proxies = {}
        proxies['http'] = f"http://{proxy['ip']}:{proxy['port']}"
        # if 'https' in proxy['protocols']:
        #     proxies['https'] = f"https://{proxy['ip']}:{proxy['port']}"
        return proxies
    
    def get(self,product):
        time.sleep(10)
        webpage = requests.get(product.url, headers=self.headers, proxies=self.proxy())
        if webpage.status_code > 500:
            print('fallo >> ', product.url)
            self.wait.append({'id':product.id, "asin": product.asin, "url":product.url})
        soup = BeautifulSoup(webpage.content, "lxml")
        return soup

class parse:
    def __init__(self, item):
        self.item = item
        self.id = self.id()
        self.asin = self.asin()
        self.url = self.url()

    def id(self):
        return (self.item.strip()).split(',')[0]
    
    def asin(self):
        return (self.item.strip()).split(',')[1]

    def url(self):
        return f"https://www.amazon.com/-/es/dp/{self.asin}"
        