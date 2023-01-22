# Сервис flower-shop

Реализация сайта онлайн заказа букетов.


## Как установить (демонстрационный вариант)

1. Загрузите проект:

```sh
git clone git@github.com:Sergryap/flower-shop.git
```

2. Перейдите в созданную директорию:

```sh
cd flower-shop
```
3. Создайте и активируйте виртуальное окружение:

```sh
python3 -m venv venv
source venv/bin/activate
```
![Снимок экрана от 2023-01-22 22-54-15](https://user-images.githubusercontent.com/99894266/213932518-83b2029e-1a20-44ea-856e-61daa6f41e21.png)


4. Установите необходимые пакеты:

```sh
pip install -r requirements.txt
```
![Снимок экрана от 2023-01-22 22-55-30](https://user-images.githubusercontent.com/99894266/213932554-829f4a52-8905-45a5-a2e6-dde315c37abf.png)


5. Выполните миграцию базы данных:

```sh
python3 manage.py migrate
```

![Снимок экрана от 2023-01-22 22-57-56](https://user-images.githubusercontent.com/99894266/213932586-62535804-bd1c-49b2-8636-f02636a572f4.png)


6. Создайте суперпользователя:

```sh
python3 manage.py createsuperuser
```
![Снимок экрана от 2023-01-22 22-58-35](https://user-images.githubusercontent.com/99894266/213932627-eefcebfc-a222-4a43-9523-6efa2b0e9612.png)


7. Запустите демонстрационную версию:

```sh
python3 manage.py runserver 0.0.0.0:8000
```

![Снимок экрана от 2023-01-22 22-59-45](https://user-images.githubusercontent.com/99894266/213932637-f992a90d-98e8-46f8-9aff-9bac4d3a462d.png)

8. Чтобы сайт не прерывал своей работы после закрытия терминала можно воспользоваться:

- Собственной инициализацией Linux (Systemd)
- Запустить последнюю команду в отдельном экране программы `screen`
- Выполнить деплой профессиональными инструментами

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
