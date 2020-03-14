# Link getter - полезный парсер ссылок. 

## Описание

Данный парсер позволяет:
* указать URL источника;
* задать лимит на количество ссылок;
* выключить рекурсивный поиск;
* обрабатывать только уникальные ссылки;
* выбрать способ вывода (экран, *.json, *.txt, *.csv);
* сохранять только ссылки с текстом (\<a href="..."\>Text\</a\>);

## Для его запуска требуется:
* Python (>=3.8)
* requests (>=2.23.0)
* beautifulsoup4 (>=4.8.2)
* lxml (>=4.5.0)

## Для запуска в виртуальном окружении используйте:
* Pipenv

## Установка с помощью setup.py:
```bash
$ cd "Path to setup.py"
$ python3 setup.py install
```

## Установка из пакета:
```bash
$ cd "Path to <package_name.whl>"
$ python3 -m pip install <package_name.whl>
```

## Пример скрипта example.py:
```python
import sys
from link_getter.core import FindLinks, Config

if __name__ == '__main__':
    config = Config(sys.argv)
    # Тут можно указать параметры
    # Они перезапишут параметры, указанные через консоль
    # config.url = 'https://yandex.ru'
    # config.completed = True
    # config.unique = True
    # ...
    finder = FindLinks(config)
    finder.find_links()
```

## Запуск через консоль:
```bash
$ cd "Path to example.py"
$ python3 example.py -url <url> [-nr, -u, -limit <n>, -completed, -screen, -json, -txt, -csv]
```

- **-nr** (no recursive) отменить рекурсивный поиск  
- **-u** (unique) сохранять и обрабатывать только уникальные ссылки  
- **-limit \<n\>** максимальное количество ссылок  
- **-completed** сохранять только ссылки с текстом
- **-screen** вывести результат в консоль в формате "текст ссылки: ссылка"  
- **-json** сохранить результаты в *.json  
- **-txt** сохранить результаты в *.txt  
- **-csv** сохранить результаты в *.csv

## Чтобы создать пакет, дополнительно требуется:
* setuptools
* wheel

## Создать пакет:
```bash
$ cd "Path to setup.py"
$ python3 setup.py bdist_wheel
```

## Дополнительная информация

Код создан в учебных целях в рамках учебного курса по веб-разработке - [otus.ru](https://otus.ru)
