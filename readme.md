## Автор Leonids Jofe

Контанты: https://t.me/LEON_JOFE
Оригинальный технический ресурс: https://www.craft.me/s/n6OVYFVUpq0o6L

## Установка и документация

Установите виртуальную среду в файле с проектом ↓
```sh
py -m venv venv
venv/scripts/activate
```

Oбновите пип-менедже ↓
```sh
python.exe -m pip install --upgrade pip
```

Установите зависимости ↓
```sh
pip install -r requirements.txt

Проверка:
	pip list
    или
	pip freeze
```

Откройте проект и установите миграцию базы данных ↓
```sh
cd .\NotificationService\

Теперь, если вы хотите протестировать этот проект с базой данных PostgreSQL,
вам нужно раскомментировать эту строку 78 в settings.py

python manage.py makemigrations
python manage.py migrate

Проверка:
	py manage.py runserver
```

Создайте админа в системе ↓
```sh
py manage.py createsuperuser
py manage.py runserver

Введите в браузере строку http://127.0.0.1:8000/admin/ и войдите в админку и создайте группу с правами.

Имя группы должно быть: common users

Добавите права:
    [add client, add mailing, add message,
    change client, change mailing, change message,
    delete client, delete mailing, delete message]

После этого перейдите в настройки пользователя администратора и добавьте его в эту группу.

Эта потребность в разрешениях и доступе.
```

Для начала простой работы запустите в разных окнах терминала ↓
```sh
py manage.py runserver
celery -A NotificationService worker -l INFO --pool=solo
```

Документация по API для интеграции с разработанным сервисом ↓
```sh
Введите в браузере строку:
	http://127.0.0.1:8000/api/

Установите свой часовой пояс:
	http://127.0.0.1:8000/api/timezone/

Добавьте клиента в базу ↓
	http://127.0.0.1:8000/api/client/
	В поле тега я обычно заполняю название страны например: lv, ru, cy.

Теперь вы можете отправить сообщение в пункт назначения:
	http://127.0.0.1:8000/api/mailing/

	Рекомендации по корректной работе приложения:
		Поле даты начала не может быть больше даты окончания, и время.

		Установленное время в поле даты начала и даты окончания нельзя вернуть
		например, если сейчас 20:22, я не могу установить 20:19. (выдаст ошибку)

		Также я не рекомендую вводить разные данные в тег.
```

Дополнительные задания ↓
```sh
5. Сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось
описание разработанного API.
Пример: https://petstore.swagger.io

7. Обеспечить интеграцию с внешним OAuth2 сервисом авторизации для административного интерфейса.
Пример: https://auth0.com

9. Удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы.
Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки.
Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.

11. Реализовать дополнительную бизнес-логику:
    добавить в сущность "рассылка" поле "временной интервал", в котором можно задать промежуток времени,
    в котором клиентам можно отправлять сообщения с учётом их локального времени.
    Не отправлять клиенту сообщение, если его локальное время не входит в указанный интервал.
```
