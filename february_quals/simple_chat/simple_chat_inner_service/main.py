from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

service_html = """
<!DOCTYPE html>
<html>
<head>
<title>Admin panel</title>
<meta property="og:image" content="https://cdn.costumewall.com/wp-content/uploads/2017/08/hackerman.jpg"/>
</head>
<body>
<p>CYBERTHON{SS3F_1N_L1n4_P3ev1ew}</p>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    client_host = request.client.host

    if client_host != "127.0.0.1":
        raise HTTPException(status_code=403,
                            detail="This service can be accessed only from the local network. Contact our system "
                                   "administrator for more info.")

    return service_html


@app.get("/api/ping")
async def ping():
    return "ok"
