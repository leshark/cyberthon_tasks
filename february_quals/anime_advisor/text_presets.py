import os

tags_metadata = [
    {
        "name": "news",
        "description": "Get all news json",
    },
    {
        "name": "test_register",
        "description": "Test registration. Returns user auth token.",
    },
    {
        "name": "test_login",
        "description": "Test login. Accepts auth token.",
    },
]

promo_json = [
    {"latest": "We are proud to announce new sign up/in functionality. Personalized anime, smart search and many more. "
               "Coming soon!"},
    {"21/01/21": "Welcome to our anime advisor site with brand new functionality! We hope you will enjoy our anime "
                 "picks!"}
]

fighting_anime = (
    ("Dragon Ball Z", os.path.join("static", "dragon.jpg")),
    ("Grappler Baki", os.path.join("static", "baki.jpg")),
    ("Hokuto no Ken. Fist of the North Star", os.path.join("static", "hakuto.jpg")),
    ("Hinomaruzumou. Hinomaru Sumo", os.path.join("static", "sumo.jpg")),
    ("Kengan Ashura", os.path.join("static", "kengan.jpg"))
)

fantasy_anime = (
    ("Fullmetal Alchemist: Brotherhood", os.path.join("static", "fullmetal.jpg")),
    ("Kaze no Tani no Nausicaä", os.path.join("static", "kaze.jpg")),
    ("Seven deadly sins", os.path.join("static", "sins.jpg")),
    ("Overlord", os.path.join("static", "overlord.jpg")),
    ("JoJo's Bizarre Adventure", os.path.join("static", "jojo.jpg"))
)

cyberpunk_anime = (
    ("Psycho-Pass", os.path.join("static", "psycho.jpg")),
    ("Ghost in the Shell", os.path.join("static", "ghost.jpg")),
    ("Akira", os.path.join("static", "akira.jpg")),
    ("Megazone 23", os.path.join("static", "Megazone.webp")),
    ("Dennou Coil", os.path.join("static", "coil.jpg"))
)

random_anime = (
    ("Gyakkyō Burai Kaiji: Ultimate Survivor", os.path.join("static", "kaiji.jpg")),
    ("Demon Slayer: Kimetsu no Yaiba", os.path.join("static", "demon_slayer.jpg")),
    ("My hero academia", os.path.join("static", "hero_acad.jpg")),
    ("Mob Psycho 100", os.path.join("static", "mob.jpg")),
    ("Cells at work", os.path.join("static", "cells.jpg")),
    ("Pop Team Epic (dangerous one)", os.path.join("static", "pop.png"))
)

admin_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>sg admin panel</title>
</head>
<body>
<h1>Ты если сюда зашел, ты - большой молодец. Представь что здесь админ типо читает твои сообщения. Ок да?</h1>
<p>{}</p>
</body>
</html>'''
