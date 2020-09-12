## 1. REgular_Task (misc)
#### Условие:
```
Мы наткнулись на файл неизвестного происхождения
Нам удалось выяснить что ценная информация
спрятана между двумя словами, в первом из которых встречаются латинские буквы bz и две цифры подряд,
а второе - длиной от 15 до 18 символов c латинскими буквами xp.
Регистр не важен. найденную строку обернуть в CYBERTHON{}
```
http://web.ctf.msk.ru/ctn2020jjkkllss/web6/REgular_Task/mess.txt
#### Как решать?
Открываем текстовый файл и видим кучу слов. Название таска намекает на использование [регулярных выражений](https://tproger.ru/articles/regexp-for-beginners/).

<b>Вариант решения номер 1:</b><br>
составляем регулярное выражение (например такое: `([\w\d]*\d{2}[\w\d]*bz[\w\d]*|[\w\d]*bz[\w\d]*\d{2}[\w\d]*)\s([\w\d]+)\s(?=\b[\w\d]{15,18}\b)[\w\d]*xp[\w\d]*`), забиваем текст в любой редактор, поддерживающий такой поиск и находим флаг.

<b>Вариант номер 2:</b><br>
то же самое, но в питоне
```
import re

with open("mess.txt") as f:
    content = f.read()

res = re.findall(r"([\w\d]*\d{2}[\w\d]*bz[\w\d]*|[\w\d]*bz[\w\d]*\d{2}[\w\d]*)\s[\w\d]+\s(?=\b[\w\d]{15,18}\b)[\w\d]*xp[\w\d]*", content, flags=re.IGNORECASE)

print(res)
```
<b>Вариант номер 3:</b><br>
Без регулярок, для сильных духом
```
with open("mess.txt") as f:
    content = f.read()

m1 = set()
m2 = set()
text = content.lower().split()

for idx, word in enumerate(text):
    if "bz" in word:
        for pair in list(zip(word,word[1:])):
            if pair[0].isdigit() and pair[1].isdigit():
                m1.add(text[idx+1])
    elif "xp" in word and 15 <= len(word) <= 18:
        m2.add(text[idx-1])

print(m1 & m2) # пересечение множеств
# Задание: доработать программу (запустите и поймите в чем проблема, исправьте)     
```


`P.S` Протестировать свои регулярные выражения можно [здесь](https://regex101.com/)<br>
`P.P.S` Кто написал регулярку короче - тот молодец


## 2. Admin1 (admin)
#### Условие:
`Говорят, самые очевидные вещи скрываются прямо перед глазами.` 
```
ssh cyberthon@194.87.95.137
password: Ricardo2020
```
#### Как решать?
Заходим на сервер по ssh(в windows можно использовать программу putty или wsl):

Смотрим файлы в домашней директории. Вспоминаем про скрытые файлы. используем команду `ls -la` для просмотра всех файлов.


![](https://storage.geekclass.ru/images/70c03648-e82b-4fd0-9e1b-2ff2963c2874.png)
Находим флаг в скрытом файле `.flag`

## 3. Admin2 (admin, ucucuga)
#### Условие:
```
Я себе построю дом,
Много места будет в нём!
Будет в доме стол и печка.
Я пущу в свой дом овечку.
Петушка пущу в свой дом,
Ну и курочку - при нём.
И корову, и козляток,
И лошадок - поросяток.
Пса с котом – само собой,
Веселее им со мной.
Гусь мне нужен для порядка,
Кто шалит – щипнёт за пятку.
Будет филин с нами жить –
Ночью домик сторожить...
Но стал я что-то сомневаться:
сисадмины согласятся?

P.S: согласились

ssh cyberthon@194.87.95.137
password: Ricardo2020
``` 
#### Как решать?
Заходим на сервер. Обращаем внимание на файл `hello.txt` если ещё не обратили ранее.

```
cyberthon@ruvds-gle8p:~$ cat hello.txt
Welcome into my big house. Please relax and enjoy the tasks.
```

Используем всю мощь ассоциативного мышления и понимаем что дом - это наш сервер. Что значит пустить в свой дом кого-то? Правильно, создать юзера. Как посмотреть список ~~жителей дома~~ пользователей сервера?<br>
`cat /etc/passwd`


```
cyberthon@ruvds-gle8p:~$ cat /etc/passwd                                        root:x:0:0:root:/root:/bin/bash                                                 daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin                                 bin:x:2:2:bin:/bin:/usr/sbin/nologin                                            sys:x:3:3:sys:/dev:/usr/sbin/nologin                                            ...                     cyberthon:x:1000:1000::/home/cyberthon:/bin/bash                                stol:x:999:999::/home/stol:/bin/false                                           pechka:x:998:998::/home/pechka:/bin/false                                       ovechka:x:997:997::/home/ovechka:/bin/false                                     petushok:x:996:996::/home/petushok:/bin/false                                   kurochka:x:995:995::/home/kurochka:/bin/false                                   korova:x:994:994::/home/korova:/bin/false                                       kozlyata:x:993:993::/home/kozlyata:/bin/false                                   loshadki:x:992:992::/home/loshadki:/bin/false                                   porosyatki:x:991:991::/home/porosyatki:/bin/false                               pes:x:990:990::/home/pes:/bin/false                                             kot:x:989:989::/home/kot:/bin/false                                             goose:x:988:988::/home/goose:/bin/false                                         philin:x:987:987::/home/philin:/bin/false                                       CYBERTHON{T00_ManY_Use3s}:x:986:986::/home/CYBERTHON{T00_ManY_Use3s}:/bin/false  
```

Имя последнего пользователя является флагом.

## 4. Admin3 (admin)
#### Условие:
`В системе обнаружен подозрительный сервис. Сможешь ли ты выяснить его тайны?`
```
ssh cyberthon@194.87.95.137
password: Ricardo2020
```
#### Как решать?

Посмотрим с каким дистрибутивом мы имеем дело:
```
cyberthon@ruvds-gle8p:~$ lsb_release -a                                         No LSB modules are available.                                                   Distributor ID: Ubuntu                                                          Description:    Ubuntu 18.04.1 LTS                                              Release:        18.04                                                           Codename:       bionic   
```
Ага, убунту версии 18.04<br>
гуглим что-то по типу:<br>
 [list all running services on ubuntu 18.04](https://websiteforstudents.com/how-to-list-all-services-running-stopped-on-ubuntu-16-04-18-04/)

 Находим команду:<br>
 `systemctl list-units --type=service`

 ```
● VErY_St3anGe.service   loaded failed | failed | Very strange systemd service.        
 ```
 Замечаем подозрительный сервис, который еще и упал.
 Смотрим информацию о статусе сервиса:

 `systemctl status VErY_St3anGe.service`

![](https://storage.geekclass.ru/images/3ed542a4-76c2-44c4-b0c6-47277d1cd2a7.png)

Замечаем что это скрипт, который запускается питоном и лежит в /usr/bin

```
cyberthon@ruvds-gle8p:~$ cat /usr/bin/script.py                                                                                         pRint("HELLO WORLD!") 
```
Вроде ничего примечательного. Пробуем посмотреть логи нашего сервиса:
`journalctl -u VErY_St3anGe.service`

![](https://storage.geekclass.ru/images/abbede68-41d8-4451-9c28-755612e91005.png)

Замечаем, что ранее файл имел другое содержание, но оно было изменено с флага на `HELLO WORLD!`

Догадаться о том, что есть возможность посмотреть логи systemd сервиса можно было посмотрев группы нашего пользователя.
```
cyberthon@ruvds-gle8p:~$ cat /etc/group
...
nogroup:x:65534:
systemd-journal:x:101:cyberthon
...
```

## 5. Gimmie_Y0u3_t0ken (web)
#### Условие:
`Мы обнаружили интересную систему авторизации. Есть ли в ней уязвимости?`<br>
http://45.143.94.76:4343/login
#### Как решать?
Заходим на сайт:

![](https://storage.geekclass.ru/images/9af8473d-0357-45a8-89d3-7a294b07043b.png)

Пробуем `admin admin`, `sql иньекцию` и нет... все не так просто.
Попробуем зарегестрировать нового пользователя:

![](https://storage.geekclass.ru/images/0e13453c-e61a-4850-9724-584a923dc161.png)

Замечаем просьбу потвердить email, поэтому укажем действительный адрес. (Например можно воспользоваться сервисом TempMail для получения почты на небольшое время)
И действительно, на почту приходит письмо с токеном потверждения почты. Переходим по ссылке и потверждаем почту.

Обращаем внимание на токен потверждения почты: `...DUIBQPU%3D%3D%3D%3D%3D%3D` <br>
Хм, интересный формат. Вернемся к нему позже.

Далее пробуем зайти в аккаунт и видим:
```
Hello, Jotaro
flag only for admin
```

Значит нам нужно зайти за админа. Вспомним про странный формат токена. `%3D%3D%3D%3D%3D%3D` является ничем другим как `=====` (url decode). А вот это уже должно быть нам знакомо. Пробуем декодировать(а как это сделать просто я расскажу на 4 мастер классе Геккона). Выясняем, что это `base32`. Декодируем токен и получаем json:
```
{"username": "Jotaro", "carma_level": 0, "luck": 0}
```

С потверждением почты мы ничего сделать не можем. Вспоминаем, что на сайте есть кнопочка `Forgot password`:

![](https://storage.geekclass.ru/images/a3abc6a3-5ad3-4325-90ee-d6096576fba4.png)

Как раз то, что нам нужно! Вставляем почту, которую мы указали при регистрации и получаем письмо с токеном аутентификации. Декодируем и подставляем в поле `username` значение `admin`
```
{"username": "admin", "carma_level": 0, "luck": 0}
```
Кодируем обратно в base32 и заходим по токену админа:
```
Hello, admin
CYBERTHON{4eck_Y0u3_T0kens}
```