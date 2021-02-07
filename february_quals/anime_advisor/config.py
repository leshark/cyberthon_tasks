from pydantic import BaseSettings


class Settings(BaseSettings):
    ip_or_domain: str
    port: str
    captcha_token: str
    captcha_site_key: str

    class Config:
        env_file = ".env"


settings = Settings()
