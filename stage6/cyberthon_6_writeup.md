## 1. Cat gallery 1 (web)
#### Условие:
```
Заказчик попросил нас провести анализ его нового инновационного сайта.
Для этого он спрятал секретную информацию в файл flag.txt в корневой директории приложения.
Сможете ли вы обнаружить уязвимость и узнать содержимое этого файла?
```
http://45.143.94.76:3200
#### Как решать?
Заходим на сайт, видим богатый(нет) функционал:

![](https://storage.geekclass.ru/images/121cc99e-07e7-44b2-bc0c-fbc71b3b5d14.png)


Внимательно изучаем ~~красивых котиков~~ ссылки:
```
?image_name=cat1.jpg
?image_name=cat2.png
?image_name=cat3.jpg
...
```

Замечаем, что это GET запрос в аргументы которого передаётся название файла. Это наводит на мысль о [LFI](https://kmb.cybber.ru/web/lfi/main.html) (local file inclusion) уязвимости. Пробуем передать в параметр `../../../../etc/passwd` и получаем интересное сообщение от сайта:
```
Hacking attempt discovered. Viewing files upper than application directory is not permitted. This incident will be reported.
```

Ага, значит сервер запрещает выходить выше корневой директории приложения. Но так это нам и не надо, по условию flag.txt, который нам нужен, как раз находится там. Подбираем кол-во `../` пока сервер не перестанет сообщать о попытке взлома. В нашем случае корневая директория находится на один уровень выше наших файлов с котиками. 

Переходим по ссылке `http://45.143.94.76:3200/?image_name=../flag.txt` и получаем флаг.



## 2. Cat gallery 2 (web)
#### Условие:

```
Заказчик продолжает развивать свой сайт.
Теперь ещё более инновационный! И безопасный! (или нет) 
```
http://45.143.94.76:3200
#### Как решать?
Переходим на сайт и оцениваем масштаб инноваций:

![](https://storage.geekclass.ru/images/66e01dfd-1756-4ec7-be0a-a3b8bda89d41.png)

Кнопка `Sign in` оказывается не рабочей, зато теперь можно выбрать категорию котиков!

![](https://storage.geekclass.ru/images/53f14ae7-0bfe-4fb2-a3b6-42de0709d7a8.png)

обращаем внимание на запрос:<br>
http://45.143.94.76:3201/`?cat_type=sad_cats`<br> 
а также на структуру html страницы:
```
<img src="static/sad_cats/cat3.jpg" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px">
...
<img src="static/sad_cats/cat1.jpg" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px">
```

Теперь еще более внимательно:<br>
?cat_type=`sad_cats`<br>
src="static/`sad_cats`/cat3.jpg"

Делаем вывод, что сервер рендерит все файлы в директории, которая передаётся в параметре GET запроса. Пробуем подставить вместо `sat_cats` параметр `./` (отображение текущей директории) и получаем:

```
<img src="static/./evil_cats" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
    
<img src="static/./sad_cats" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
    
<img src="static/./future_cats" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
    
...  

<img src="static/./fat_cats" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
```
Сервер пытается отрендерить буквально все, даже директории.

Стоп, вы тоже это видите? ~~[Directory traversal](https://en.wikipedia.org/wiki/Directory_traversal_attack) уязвимость!~~ `static/./future_cats`. Это же кошки из будущего! Смотрим что находится в этой директории:<br>
url/?cat_type=`future_cats`

```
<img src="static/future_cats/cat1.jpg" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
    
<img src="static/future_cats/edff72b33bfc4973.txt" alt="cool_cat" style="width: 200px; height: 200px; margin: 20px"/>
```

Замечаем подозрительный файл `edff72b33bfc4973.txt`, переходим по ссылке `site_url/static/future_cats/edff72b33bfc4973.txt` и получаем флаг.

## 3. Cat gallery 3 (web)
#### Условие:
```
Заказчик исправил все ранее найденные уязвимости и продолжает внедрять фичи!
Теперь он полностью уверен, что его сайт в абсолютной безопасности!
Убеди его в обратном.
```

http://45.143.94.76:3202/

#### Как решать?
Переходим по ссылке, видим старый добрый сайт с котиками, вроде ничего не изменилось. А нет, добавились формы входа и регистрации:

![](https://storage.geekclass.ru/images/61173c01-8a8c-439d-bf8d-956b2d66f46b.png)


![](https://storage.geekclass.ru/images/94c005bb-5646-4845-9201-c55dc882da4c.png)

Сразу пробуем ковычку, но безрезультатно:<br>
`Username contains invalid characters!`<br>
Перебором понимаем, что запрещены ещё символы `[ ] _`

Пробуем зарегестрировать простого пользователя, например `DIO`<br>
Обратим внимание на то, что появилась сессия<br>
`eyJ1c2VybmFtZSI6eyIgdCI6WyJESU8iLCJrYWJhY2hraSJdfX0.XnYRtQ.YDaC7kG-_ki8BLYn8lKPPlLoI1M`<br>
Декодируем её:
```
{
 "username": {
  " t": [
   "DIO",
   "kabachki"
  ]
 }
}
```

Возвращаемся на главную страницу и видим `Welcome, DIO`, а значит наш юзернейм подставился в html страницу.
```
<a id="next" href="http://tiny.cc/d7hilz">Welcome, DIO</a>
<!-- TODO: add logout and funny cat name generator in template -->
```

Препдполагаем [SSTI](https://portswigger.net/research/server-side-template-injection) (Server Side Template Injection) уязвимость. Учитывая, что  сервер написан на фласке (видно в заголовках HTTP ответа - `Server: Werkzeug/1.0.0 Python/3.7.4`) скорее всего шаблонизатором(движок, который рендерит html на бэкенде) является jinja.

Пробуем зарегестрировать юзера `{{34.5*2}}` и:

![](https://storage.geekclass.ru/images/ef740dbb-3cad-4266-b5dc-26d7db546c96.png)

Nice. Как говорится, `вижу уязвимость`. Дальше усиленно гуглим и пробуем вывести все, что можем, учитывая фильтрацию символов при регистрации. Например `{{config.items()}}` выводит список конфигурационных переменных:

![](https://storage.geekclass.ru/images/9902a37a-1230-485f-bf79-6f0c49a416bb.png)

Там и находился флаг.

P.S. внимательные участники заметили, что секретный ключ фласка также был доступен, и тем самым можно было подписать сессию и отправить уязвимость без фильтрации символов, что привело бы к получению доступа к серверу (`RCE`)

Тот самый, уязвимый участок кода:
```
# let's pretend all html is processed with render_template_string
user = render_template_string(session["username"][0])
```

## 4. INSANE (insane,reverse,stego,crypto,misc,ppc)
#### Условие:
```
INSANE INSANE INSANE
https://yadi.sk/d/GM5yHpy-sW6oPw
```
#### Как решать?

скачиваем app.apk файл, запускаем его на устройстве(опционально):

![](https://storage.geekclass.ru/images/c73753d9-68ac-4d26-8759-4348d30676a8.png)

Продолжаем расследование. Берём `apktool` `dex2jar` и `jdgui`.
в итоге получаем исходный код приложения:
```
@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ImageView imageView = findViewById(R.id.imageDisplay);
        imageView.setImageResource(R.drawable.hello);
        // imageView.setImageResource(R.drawable.flag);
    }
```

Замечаем комментарий `imageView.setImageResource(R.drawable.flag);`. Идем в папку с ресурсами, которую нам дал apktool, находим файл `flag.png`:

![](https://storage.geekclass.ru/images/fbb41a1b-c6f0-45bd-83d5-8e509d418bcf.jpg)

Вот это поворот! Ну стега и стега, смотрим что там внутри. Обращаем внимание на exif поля:
```
Artist - Ti dumal eto stega
Copyright - no eto bila ya
OwnerName - Crypta
ImageDescription - jppni://nmipotqz.ags/UiM1Wa3r
```

`jppni://nmipotqz.ags/UiM1Wa3r` подозрительно похоже на url адрес, чем-то зашифрованный. Пробуем разные классические шифры(например на www.dcode.fr), в итоге подходит аффинный. (Догадаться можно было по остальным exif меткам: `city - Affine`)

Получаем ссылку на пастебин:<br>
`https://pastebin.com/QsA1Uc3x`

В ней находится код на эзотерическом языке программирования brainfuck. Вбиваем его в любой онлайн декодер и получаем:
```
ti dumal eto misc, no eto bil ya, admin!
ssh cyberthon@194.87.95.137 Ricardo2020
```

Заходим по ssh на сервер и сразу видим файлы:
```
data.txt
task.txt
```

Читаем task.txt - `Найди в файле data.txt уникальную строчку`

Решение - `cat data.txt | sort | uniq -u`<br>
Вывод - `0KLRiyDQtNGD0LzQsNC7INGN0YLQviDQsNC00LzQuNC9PyDQndC+INGN0YLQviDQsdGL0Lsg0Y8sINCy0LXQsSEKaHR0cDovLzQ1LjE0My45NC43Njo0MjA4Lw==`<br>

Декодим base64:
```
Ты думал это админ? Но это был я, веб!
http://45.143.94.76:4208/
```

На сайте видим:
```
Here you get 624 random numbers. Can you predict 625 one?
624 числа через |
```

Но как же нам отгадать 625 число? Мы же не можем видеть будущее...

![](https://storage.geekclass.ru/images/fa43140e-ceb7-4dd4-9f3b-525e884c826d.png)

Или можем? Все дело в том, что random в питоне является [псевдослучайным](https://habr.com/ru/post/137864/), а значит, набрав достаточно данных мы можем восстановить исходное состояние системы!

Код на питоне (понадобится библиотека `randcrack`):
```
from randcrack import RandCrack

rc = RandCrack()
numbers = [] # все числа с сайта

for number in numbers:
    rc.submit(number)

print(rc.predict_randint(0, 4294967291)) # верхней границей выбираем самое большое число выборки
```

Вводим предсказанное число и получаем флаг.