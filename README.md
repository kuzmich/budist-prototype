##Настройка
    1. Клонируем репозиторий
    $ git clone git://github.com/kuzmich/budist-prototype.git

    2. Создаем virtualenv 
    $ mkvirtualenv some-name-here
    or
    $ virtualenv dir-for-virtenv

    3. Ставим нужные пакеты
    $ pip install -r requirements.txt

    4. Ставим MongoDB и RabbitMQ

#Использование
    Заполним базу объектами
    $ ./initialize_db.py 

    Запустим celery workers
    $ celery -A tasks worker --loglevel=debug -B

#Идея
Безусловно, реализовать все это можно десятками способов. Я постарался сделать прототип максимально простым.

У будильника 2 основных атрибута - время срабатывания и дата либо день недели (для периодических).
Ну и пользователь, кому этот будильник принадлежит. Про дополнительные будильники не совсем понятно, кто/когда
их заводит - в любом случае они вписываются в эту модель, только создание их идет в нужном месте.

Объекты с этими атрибутами лежат в коллекции MongoDB 'alarms'. В коллекции 'users' - соответственно пользователи.

Теперь нам нужно, что бы кто-то периодически проверял, не пора ли кому-нибудь позвонить.
Я эту задачу отдал scheduler-у celery. Он гибкий и удобный. Он вызывает задачу tasks.find() раз в минуту.

Tasks.find() ищет будильники, у которых время срабатывания равно текущему времени,
и либо совпадает дата, либо день недели. Для 1 061 280 объектов в коллекции Mongo делает это достаточно шустро.
Индексы занимают в районе 100M.

Затем tasks.find() вызывает tasks.call(), передавая в функцию нужные аттрибуты - профиль пользователя с телефоном и т.д.

И все по-новой. В логе celery видим, что раз в минуту система звонит 3 товарищам. Вуаля.

Что касается менеджера будильников, тут вообще все просто - найти/создать/удалить соответствующий объект в базе Mongo
не составляет труда.