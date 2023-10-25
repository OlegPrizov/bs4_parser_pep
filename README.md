# Парсер документации Python

## Описание
Этот парсер умеет:
1. Собирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей.
2. Собирать информацию о статусах версий Python.
3. Скачивать архив с актуальной документацией.
4. Собирать данные о документах PEP, считать их количество в каждом статусе и 
общее количество PEP, а также сравнивать статусы на главной странице со статусами в 
отдельной карточке PEP.

Парсер работает в разных режимах через аргументы командной строки. В него 
включено логирование и обработка ошибок.

<details>
  <summary><h2> Запуск проекта </h2></summary>

- Клонируйте репозиторий и перейдите в него:

```bash
git clone git@github.com:OlegPrizov/bs4_parser_pep.git
cd bs4_parser pep
```

- Cоздайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
. venv/scripts/activate
```

- Обновите `pip` и установите зависимости из файла `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Запустите парсер:
```bash
python src/main.py {режим работы парсера} [-ключ аргумент]
```

</details>

<details>
  <summary><h2> Режимы работы парсера </h2></summary>

- ### `whats-new`
    Этот парсер собирает ссылки на статьи о нововведениях в Python, переходит
    по ним и забирает информацию об авторах и редакторах статей:
    ```bash
    python main.py whats-new [-ключ аргумент]
    ```

- ### `latest_versions`
    Этот парсер собирает информацию о статусах версий Python.
    ```bash
    python main.py latest-versions [-ключ аргумент]
    ```

- ### `download`
    Этот парсер скачивает архив с документацией Python.
    ```bash
    python main.py download [-ключ аргумент]
    ```

- ### `pep`
    Этот парсер получает данные обо всех документах PEP, сравнивает статус на 
    странице PEP со статусом в общем списке (при несоответсвии информация 
    выводится в логи), подсчитывает количество PEP в каждом статусе и общее 
    количество PEP.
    ```bash
    python main.py pep [-ключ аргумент]
    ```

</details>

<details>
  <summary><h2> Опциональные аргументы </h2></summary>

- Справка о режимах работы парсера и синтаксисе: `-h, --help`
```bash
python main.py -h
```

- Очистка кеша перед выполнением парсинга: `-c, --clear-cache`
```bash
python main.py {режим работы парсера} -c
```

- Дополнительные способы вывода данных: `-o {pretty,file}, --output {pretty,file}`
    - `pretty` - выводит данные в командной строке в таблице
    ```bash
    python main.py {режим работы парсера} -o pretty
    ```

    - `file` - сохраняет информацию в файл `.csv` в папку `results/`
    ```bash
    python main.py {режим работы парсера} -o file
    ```

</details>
