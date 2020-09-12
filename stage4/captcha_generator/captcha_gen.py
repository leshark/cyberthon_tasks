import hashlib

from PIL import Image, ImageDraw, ImageFont
from random import randint
import os
import json

answers = {}


def gen_captcha(example, filename):
    img = Image.new('RGB', (200, 30), color=(255, 255, 255))

    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('Arial.ttf', 15)
    d.text((10, 10), example, font=fnt, fill=(0, 0, 0))

    img.save(filename, optimize=True, quality=200)


def gen_example():
    num1 = randint(0, 99)
    num2 = randint(0, 1000)
    num3 = randint(0, 9)
    num4 = randint(0, 99)
    example = f"{num1} + ({num2} * {num3}) - {num4}"
    return example, eval(example)


def generate(captcha_num):
    for i in range(captcha_num):
        ex, ans = gen_example()
        answers[i] = ans
        filename = os.path.join("static", hashlib.md5(f"captcha{i}".encode()).hexdigest() + ".png")
        gen_captcha(ex, filename)
    with open("answers.json", "w") as f:
        json.dump(answers, f)
