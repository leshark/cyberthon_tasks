import random
import subprocess
from typing import Optional
from uuid import uuid4

import jwt
from fastapi import FastAPI, Request, Form, UploadFile, BackgroundTasks, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import settings
from text_presets import tags_metadata, promo_json, fighting_anime, fantasy_anime, cyberpunk_anime, random_anime, \
    admin_page
from validators import validate_suggestion_data

FLAG1 = "CYBERTHON{P30tec4_Y0u3_EndP01ntS}"

app = FastAPI(openapi_tags=tags_metadata)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

info_log = open("info.log", "a")
error_log = open("error.log", "a")


def choose_anime(anime_type):
    if anime_type == "fighting":
        return random.choice(fighting_anime)
    elif anime_type == "fantasy":
        return random.choice(fantasy_anime)
    elif anime_type == "cyberpunk":
        return random.choice(cyberpunk_anime)
    else:
        return random.choice(random_anime)


def process_suggestion_data(filename):
    return subprocess.run(["node", "xss_bot_pupet.js", app.url_path_for("render_admin_page") + f"?filename={filename}"],
                          timeout=10, stderr=error_log, stdout=info_log)


class User(BaseModel):
    name: str


@app.middleware("http")
async def add_help_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-server-name"] = "FastAPI"
    return response


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "captcha_site_key": settings.captcha_site_key})


@app.get("/api/ping")
async def ping():
    return "ok"


@app.get("/api/news", tags=["news"])
async def get_news():
    return promo_json


@app.post("/get_anime", response_class=HTMLResponse)
async def get_anime(request: Request, anime_type: str = Form(...)):
    anime_result = choose_anime(anime_type)
    return templates.TemplateResponse("index.html", {"request": request, "anime_name": anime_result[0],
                                                     "img_path": anime_result[1],
                                                     "captcha_site_key": settings.captcha_site_key})


@app.post("/send_suggestion")
async def send_suggestion(background_tasks: BackgroundTasks,
                          tittle: str = Form(...),
                          description: str = Form(...),
                          file: Optional[UploadFile] = File(b''),
                          g_recaptcha_response: str = Form(..., alias="g-recaptcha-response")
                          ):
    if file:
        validate_resp = await validate_suggestion_data(tittle,
                                                       description,
                                                       file.filename,
                                                       g_recaptcha_response
                                                       )
        if validate_resp == "Admin will view your problem/suggestion very soon!":
            background_tasks.add_task(process_suggestion_data, file.filename)
    else:
        validate_resp = await validate_suggestion_data(tittle,
                                                       description,
                                                       "",
                                                       g_recaptcha_response
                                                       )
    return validate_resp


# bot page for xss render
@app.get("/api/sg-admin-panel", response_class=HTMLResponse, include_in_schema=False)
async def render_admin_page(filename: str):
    return admin_page.format(filename)


@app.post("/api/test_register", tags=["test_register"])
async def test_register(user: User):
    user_token = jwt.encode({"user_id": f"{uuid4().hex}", "name": user.name, "is_admin": False}, "secret",
                            algorithm="HS256")
    return user_token


@app.post("/api/test_login", tags=["test_login"])
async def test_login(token: str):
    try:
        user_data = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return "invalid jwt token"
    if user_data.get("is_admin"):
        return FLAG1
    return "You have successfully logined"
