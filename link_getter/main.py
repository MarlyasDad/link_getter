import sys
from link_getter.core import FindLinks, Config


def main():
    config = Config(sys.argv)
    # config.url = 'https://yandex.ru'
    # config.completed = True
    # config.unique = True
    # ...
    finder = FindLinks(config)
    finder.find_links()


if __name__ == '__main__':
    main()
