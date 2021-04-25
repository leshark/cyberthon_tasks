import sys
import random

intro_text = """
  ______                                   __                               _               _          
 |  ____|                                 / _|                             | |             | |         
 | |__    ___   ___  __ _  _ __    ___   | |_  _ __  ___   _ __ ___      __| | _   _  _ __ | | __ __ _ 
 |  __|  / __| / __|/ _` || '_ \  / _ \  |  _|| '__|/ _ \ | '_ ` _ \    / _` || | | || '__|| |/ // _` |
 | |____ \__ \| (__| (_| || |_) ||  __/  | |  | |  | (_) || | | | | |  | (_| || |_| || |   |   <| (_| |
 |______||___/ \___|\__,_|| .__/  \___|  |_|  |_|   \___/ |_| |_| |_|   \__,_| \__,_||_|   |_|\_\\__,_|
                          | |                                                                        
                          |_|                                                                        
"""

with open("durka.txt", encoding="utf-8") as durka:
    intro_img = durka.read()

builtins_dct = {
    '__builtins__': {
        'print': print,
        'globals': globals,
        'locals': locals,
        'getattr': getattr
    }
}


def f():
    flag = "CYBERTHON{P0we3_0f_Pyt40n_1ntr0Spec4i0n}"
    return "Otdai kolpak!"


def main():
    kolpak = f
    while True:
        try:
            text = input(">>> ")
            if "exec" in text or "_" in text or "." in text or " " in text or '"' in text:
                print(
                    random.choice(
                        (
                            "Понятно. А теперь в палату.",
                            "Ты как смирительную рубашку снял?",
                            "Бегом в палату лоботомию делать.",
                            "Ясно. Увозим его, мужики.",
                            "Два кубика галоперидола, срочно.",
                            "Ага, попался! В процедурную его, в процедурную.",
                        )
                    )
                )
                continue
            else:
                eval("print(" + text + ")", builtins_dct, locals())
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"С такими приколами ({str(e)}) тебе сам знаешь куда.")


if __name__ == "__main__":
    print(intro_text)
    print(intro_img)
    del intro_text
    del intro_img
    del durka
    main()
