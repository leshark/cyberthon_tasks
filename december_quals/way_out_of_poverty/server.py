import random

FLAG = "CYBERTHON{l1fe_s1mu1at03}"

balance = 50
thirsty = 3
hungry = 7

current_step = 1
steps_with_ponzi = 0
ponzi_enabled = False

options = '''
1. работать (+15$)
2. купить еды (-10$)
3. купить воды (-5$)
4. пригласить двух друзей вложиться в прибыльную схему (+30$ каждый ход)
5. купить билет в Калифорнию (-1000$)
'''

def check_life():
    global steps_with_ponzi
    global balance

    if balance < 0:
        print("Вас арестовали за кражу")
        return True
    if thirsty < 0:
        print("Вы умерли от обезвоживания. С кем не бывает")
        return True
    elif hungry < 0:
        print("Говорила мама кушать вовремя... Теперь уже поздно")
        return True
    
    if steps_with_ponzi >= 14:
        print("Ваша инвестиционная схема развалилась, а вы посажены за мошенничество")
        return True
    if ponzi_enabled:
        balance+=30
        steps_with_ponzi +=1

def buy_water():
    global thirsty
    global balance
    thirsty += 3
    balance -= 5

def buy_food():
    global hungry
    global balance
    hungry = 7
    balance -= 10

def ponzi_scheme():
    global ponzi_enabled

    if not ponzi_enabled:
        ponzi_enabled = True
        print("Удачные инвестиции. Наверное")
    else:
        print("У вас было всего двое друзей, позвать больше не выйдет((")

def do_work():
    global balance
    num1 = random.randint(1,100)
    num2 = random.randint(1,100)
    print("На работе вам дают сложную задачу, решите ее: {} + {} = ?".format(num1, num2))
    user_inp = input("Ответ: ")
    if int(user_inp) == num1 + num2:
        balance+=15
        print("Отлично, завтра будут еще интересные задачи")
    else:
        print("Вы не смогли решить это сложнейшую задачу. Что ж, попробуйте завтра")

def buy_ticket():
    if balance >= 1000:
        print("Как вам удалось накопить столько денег? Ну ладно, вот номер вашего билета - {}".format(FLAG))
        return True
    else:
        print("Недостаточно денег. Зря в очереди стояли!")

actions = {"1":do_work, "2":buy_food, "3":buy_water, "4":ponzi_scheme, "5":buy_ticket}

print("Помоги Стэнли накопить на переезд\n"
      "Каждый день вы можете выбирать одно из предложенных действий\n"
      "Начальный капитал - 50$\n"
      "-------------------")

while True:
    if check_life():
        break
    print("Новый день. Ход {}. Ваш баланс - {}$.".format(current_step, balance))
    print(options)
    action = input("введите номер действия: ")
    res = actions.get(action, lambda: print("Некорректное действие!"))()
    if res:
        break
    thirsty -= 1
    hungry -= 1
    current_step +=1
    print("-------------------")
