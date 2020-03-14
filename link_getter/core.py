from datetime import datetime
import json
import csv
from queue import Queue
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup
import requests


class Config:
    url: str
    recursive: bool
    limit: int
    unique: bool
    completed: bool
    json: bool
    txt: bool
    csv: bool
    screen: bool

    def __init__(self, argv: Optional[list] = None) -> None:
        if not argv:
            argv = []
        self.url = ''
        self.json = False
        self.txt = False
        self.csv = False
        self.screen = False
        self.recursive = True
        self.unique = False
        self.completed = False
        self.limit = 100
        self.init_input_args(argv)

    def init_input_args(self, argv: list) -> None:
        """
        -nr, -u, -limit <n>, -screen, -json, -txt, -csv
        """
        for key, arg in enumerate(argv):
            if arg == '-json':
                self.json = True
            if arg == '-txt':
                self.txt = True
            if arg == '-csv':
                self.csv = True
            if arg == '-screen':
                self.screen = True
            if arg == '-limit':
                if len(argv) >= key + 1:
                    if argv[key + 1].isdigit():
                        self.limit = int(argv[key + 1])
            if arg == '-url':
                if len(argv) >= key + 1:
                    if not argv[key + 1].startswith('-'):
                        self.url = argv[key + 1]
            if arg == '-nr':
                self.recursive = False
            if arg == '-u':
                self.unique = True
            if arg == '-completed':
                self.completed = True


Link = Tuple[str, str]


class LinksContainer:
    count: int
    links: List[Link]
    keys: set
    config: Config

    def __init__(self, config: Config) -> None:
        self.count = 0
        self.keys = set()
        self.links = []
        self.config = config

    def check_exists(self, url: str) -> bool:
        if url in self.keys:
            return True
        if url.endswith('/'):
            if url[:-1] in self.keys:
                return True

    def add_link(self, link: Link) -> bool:
        link_text = link[1]
        if link_text == '' and self.config.completed:
            return False
        link_url = link[0]
        if self.check_exists(link_url) and self.config.unique:
            return False
        self.links.append(link)
        self.keys.add(link_url)
        self.count += 1
        return True

    def get_all_links(self) -> List[Link]:
        return self.links


class LinkPrinter:
    links: List[Link]
    config: Config

    def __init__(self, links: LinksContainer, config: Config) -> None:
        self.links = links.get_all_links()
        self.config = config

    def to_txt(self, date_string: str) -> None:
        with open(f'links_txt_{date_string}.txt', 'w') as file:
            for link in self.links:
                file.write(f'{link[0]} : {link[1]}\n')

    def to_json(self, date_string: str) -> None:
        json_text = json.dumps(self.links, indent=4, ensure_ascii=False)
        with open(f'links_json_{date_string}.json', 'w') as file:
            file.write(json_text)

    def to_csv(self, date_string: str) -> None:
        with open(f'links_csv_{date_string}.csv', 'w', encoding="utf-8-sig", newline='') as csvfile:
            fieldnames = ['URL', 'Text']
            writer = csv.writer(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames)
            for link in self.links:
                writer.writerow([link[0], link[1]])

    def to_screen(self) -> None:
        for link in self.links:
            print(f'{link[0]} : {link[1]}')

    def print(self) -> None:
        date_of_create: str = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        if self.config.json:
            self.to_json(date_of_create)
        if self.config.txt:
            self.to_txt(date_of_create)
        if self.config.csv:
            self.to_csv(date_of_create)
        if self.config.screen:
            self.to_screen()


class FindLinks:
    container: LinksContainer
    heap: Queue
    url: str
    first_link: Link

    def __init__(self, config: Config):
        self.url = config.url
        # self.limit = config.limit
        self.container = LinksContainer(config)
        self.printer = LinkPrinter(self.container, config)
        self.heap = Queue()
        self.initialize_first_request()

    def initialize_first_request(self):
        if self.url == '':
            print('Start point is not defined. Please, restart the application with -url parameter!')
            exit()
        if not self.url.startswith('http'):
            self.url = f'http://{self.url}'
        # Initialize first request
        self.first_link: Link = (self.url, 'Entry point')
        self.heap.put(self.first_link)
        self.container.add_link(self.first_link)

    @staticmethod
    def get_raw_html(url: str) -> str:
        try:
            r = requests.get(url, allow_redirects=True, timeout=1)
        except requests.exceptions.ConnectionError:
            return ''
        if r.status_code != 200:
            return ''
        return r.text

    def find_all_links_from_raw_html(self, raw_html: str) -> List[Link]:
        found_links = []
        soup = BeautifulSoup(raw_html, 'lxml')
        links = soup.find_all('a', href=True)
        for link in links:
            absolute_url: Optional[str] = self.make_absolute_url(link['href'])
            if not absolute_url:
                continue
            found_link: Link = (absolute_url, link.text)
            found_links.append(found_link)
        return found_links

    def make_absolute_url(self, url: str) -> Optional[str]:
        absolute_url: str = url
        if not url.startswith('http'):
            if not url.startswith('/'):
                return None
            absolute_url = f'{self.url}{url}'
        return absolute_url

    def find_links(self) -> None:
        print(f'Started at {datetime.now()}')
        print(f'Finding {self.container.config.limit} links...')
        running: bool = True
        while running:
            if self.heap.empty():
                break
            next_link = self.heap.get()
            url = next_link[0]
            response: str = self.get_raw_html(url)
            found_links: List[Link] = self.find_all_links_from_raw_html(response)
            # Все найденные ссылки добавляем в хранилище ссылок и в очередь на обработку
            for link in found_links:
                success = self.container.add_link(link)
                # Если ссылка новая, добавить её в очередь на переход
                if success:
                    self.heap.put(link)
                # Выходим если достигли лимит или все ссылки обработаны
                if self.container.config.limit <= self.container.count:
                    running = False
                    break

        self.printer.print()
        print(f'Finished at {datetime.now()}')
        print(f'Found links: {self.container.count}')
