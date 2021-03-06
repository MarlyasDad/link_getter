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
$ python3 example.py -url <url> [-nr, -f, -u, -limit <n>, -completed, -level <n>, -screen, -json, -txt, -csv]
```

- **-url \<url\>** стартовая страница (обязательный параметр)  
- **-nr** (no recursive) отменить рекурсивный поиск, искать по уровням \*  
- **-f** (first only) искать только на стартовой странице (уровень 0)  
- **-u** (unique) сохранять и обрабатывать только уникальные ссылки  
- **-limit \<n\>** максимальное количество ссылок (по умолчанию 100)  
- **-level \<n\>** глубина поиска (только для рекурсивного поиска, по умолчанию 100 уровней вложенности)  
- **-completed** сохранять только ссылки с текстом (\<a href="..."\>Text\</a\>)  
- **-screen** вывести результат в консоль в формате "текст ссылки: ссылка"  
- **-json** сохранить результаты в *.json  
- **-txt** сохранить результаты в *.txt  
- **-csv** сохранить результаты в *.csv

\* Поиск по уровням работает по следующему принципу: сначала ищем все ссылки на стартовой (уровень 0), потом проходим по всем ссылкам, которые нашли на уровне 0 (уровень 1), потом по всем ссылкам, которые нашли на уровне 1 (уровень 2) и т.д.

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
