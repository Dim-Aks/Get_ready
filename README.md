# Get_ready!

A website for friends who want to see each other more often.
On the "Get_ready!" website, registered friends can create slots for their desired meetings.
In the slots, they can specify: date, place, dress code, and even attach a link to the event, as well as schedule the event or give a detailed description of it.
Each user can view the entire list of meetings, filter them by relevance, or view only their meetings. You can even take a look at what meetings have already taken place.
Also in the event card, friends can discuss all the details in the comments.

There is no limit to the improvements, the plans include: notifications to meeting participants about the creation and comments, a picture to the user's profile, add top gifs to the main page :)


# Собирайся!

Сайт для друзей, которые хотят видеться чаще.
На сайте "Собирайся!" зарегистрированные пользователи - друзья могут создавать слоты на желаемые встречи.
В слотах они могут указать: дату, место, дресс-код и даже приложить ссылку на мероприятие, а также расписать мероприятие или дать его подробное описание.
Каждый пользователь может просматривать как весь список встреч, так и отфильтровать их по актуальности, или посмотреть только свой встречи. Можно даже глянуть, какие встречи уже прошли.
Также в карточке мероприятия друзья могут обсудить все детали в комментариях.

Нет предела улучшениям, в планах: уведомления участникам встречи о создании и комментариях, картинку к профилю пользователя, добавить топовые гифки на главную :)

Мой Телеграмм: @Dim_Ax


# ⚙️ Требования

- asgiref==3.8.1
- colorama==0.4.6
- coverage==7.8.0
- Django==5.1.7
- factory_boy==3.3.3
- Faker==37.1.0
- iniconfig==2.1.0
- packaging==24.2
- pluggy==1.5.0
- pytest==8.3.5
- pytest-cov==6.1.1
- pytest-django==4.11.1
- sqlparse==0.5.3
- tzdata==2025.1

 # 🛠 Установка

Клонировать репозиторий:

git clone https://github.com/Dim-Aks/Get_ready.git

cd get_ready

Создать виртуальное окружение:

python -m venv venv

source venv/bin/activate  - Linux/Mac

venv\Scripts\activate  - Windows

Установить зависимости:

pip install -r requirements.txt

Настройка переменных окружения:

cp .env.example .env

Заполнить .env своими значениями.

Запуск миграций:

python manage.py migrate

Запуск сервера:

python manage.py runserver

Для доступа к страницам сайта, кроме главной, нужно создать пользователя:

python manage.py createsuperuser

cледуйте интерактивным инструкциям

# 🧪 Тестирование

Запуск тестов:

pytest --cov

# 📬 Контакты
Автор: Дмитрий

Email: kiton444@gmail.com

Telegram: @Dim_Ax
