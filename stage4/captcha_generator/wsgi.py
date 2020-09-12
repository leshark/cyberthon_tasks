from app import app, CAPTCHA_NUM
from captcha_gen import generate

import os

if len(os.listdir("static")) <= 1:
        generate(CAPTCHA_NUM)

if __name__ == '__main__':
    app.run()