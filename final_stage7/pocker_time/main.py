import random

from treys import Card
from treys import Deck
from treys import Evaluator

evaluator = Evaluator()
board = []
total_rounds_won = 0
ROUNDS = 15
funny_answers = ["Ну вот, я проиграл свой дом, машину, жену и две почки",
                 "Ты знаешь какие были ставки??? Теперь я в долгу у TEIAI corp на 700 миллионов ¥!",
                 "КАКОГО ЧЕРТА КАРТЫ В ЗАПЕЧАТАННОЙ КОЛОДЕ В ДРУГОМ ПОРЯДКЕ РАЗЛОЖЕНЫ...",
                 "https://abandonedfactory.files.wordpress.com/2011/09/kaiji2-23-2.png?w=640&h=360",
                 "https://www.youtube.com/watch?v=nRJtk0KjDQk"
                 ]

print("Привет, я тут засел в техасский дро покер. Поможешь мне?\n"
      "Я даю тебе шесть рук, а ты мне говоришь номер сильнейшей.\n"
      "На все про все даю тебе 60 секунд. По рукам?")

while total_rounds_won < ROUNDS:

    deck = Deck()
    deck.shuffle()

    hands = {}

    for hand_num in range(6):
        hand = deck.draw(5)
        print("Рука игрока {}:".format(hand_num + 1),
              " ".join(Card.print_pretty_card(card).replace("[", "").replace("]", "") for card in hand))

        score = evaluator.evaluate(board, hand)
        hands[score] = hand_num + 1

    answer = hands[min(hands)]
    user_inp = input("Номер выигрывающей руки: ")
    try:
        if int(user_inp) == answer:
            print("Отлично, следующий раунд!" if total_rounds_won + 2 < ROUNDS else "Ура! Я выиграл эту партию!")
            total_rounds_won += 1
        else:
            print(random.choice(funny_answers))
            break
    except Exception:
        print("Что-то пошло не так")
        exit(0)
else:
    print("CYBERTHON{p30_p0cke3_p1aye3}")
