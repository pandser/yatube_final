# Социальная сеть для блогеров Yatube

Сайт на котором возможно создать свою страницу. Автор может выбрать имя и уникальный адрес для своей страницы.
При переходе на страницу автора можно увидеть все его посты. Зарегестрированный пользователь может оставить комментарий под постом, а также подписаться на автора.
Записи можно отправить в группу и посмотреть там посты других авторов.

Цель проекта, изучить работу с фреймворком Django, разобраться с архитектурой MVT.

## Технологии

- Python 3.7
- Django 2.2
- HTML
- CSS(Bootstrap)

## Запуск проекта в dev-режиме

1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
        git clone <ссылка с git-hub>
    ```

2. Cоздать виртуальное окружение:

    windows

    ```bash
        python -m venv venv
    ```

    linux

    ```bash
        python3 -m venv venv
    ```

3. Активируйте виртуальное окружение

    windows

    ```bash
        source venv/Scripts/activate
    ```

    linux

    ```bash
        source venv/bin/activate
    ```

4. Установите зависимости из файла requirements.txt

    ```bash
        pip install -r requirements.txt
    ```

5. В папке с файлом manage.py выполните команду:

    windows

    ```bash
        python manage.py runserver
    ```

    linux

    ```bash
        python3 manage.py runserver
    ```

