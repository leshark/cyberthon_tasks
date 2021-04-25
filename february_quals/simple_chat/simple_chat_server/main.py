import logging
import random
from ipaddress import ip_network, ip_address
from urllib.parse import urlparse

from fastapi import FastAPI
from linkpreview import link_preview

app = FastAPI()

song_text = '''
We're no strangers to love
You wouldn't get this from any other guy
You know the rules and so do I
Your heart's been aching, but
Never gonna let you down
Gotta make you understand
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Never gonna make you cry
Never gonna give, never gonna give
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna tell a lie and hurt you
Never gonna run around and desert you
We've known each other for so long
Never gonna say goodbye
Never gonna give you up
Inside, we both know what's been going on
A full commitment's what I'm thinking of
You're too shy to say it'''.split("\n")

local_networks = [ip_network('10.0.0.0/8'), ip_network('172.16.0.0/12'), ip_network('192.168.0.0/16'),
                  ip_network('127.0.0.0/8')]


def get_preview_for_link(link):
    preview = link_preview(link, parser="lxml")
    return {
        "status": "success",
        "tittle": preview.force_title if not preview.title else (preview.title if preview.title else ""),
        "image_url": preview.absolute_image if not preview.image else (preview.image if preview.image else ""),
        "description": preview.description if preview.description else ""
    }


async def parse_url(link):
    try:
        result = urlparse(link)
        if result.scheme not in ["http", "https"]:
            return "scheme can be only http(s)"

        domain_or_ip = result.hostname

        try:
            ip_addr = ip_address(domain_or_ip)
            if ip_addr and all(ip_addr not in subnet for subnet in local_networks):
                return "success"
            else:
                return "can't preview local ip address"
        except ValueError:
            return "success"

    except ValueError:
        return "not a url"
    except Exception as e:
        logging.error(e, exc_info=True)
        return "unknown error"


@app.get("/api/preview")
async def gen_preview(link: str):
    parse_status = await parse_url(link)
    if parse_status == "success":
        logging.info(f"Got valid url: {link}")
        return get_preview_for_link(link)
    return {"status": parse_status}


@app.get("/api/ping")
async def ping():
    return "ok"


@app.get("/api/generate")
async def gen_text():
    return random.choice(song_text)
