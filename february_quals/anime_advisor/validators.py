import requests
import config


def check_captcha(captcha_prompt):
    return requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": config.settings.captcha_token, "response": captcha_prompt}
    ).json().get("success")


async def validate_suggestion_data(tittle, descr, filename, captcha_code):
    if any(symbol in tittle for symbol in [">", "<", "&", "'", "\""]):
        return "Found invalid symbols, please resubmit your suggestion!"
    if any(symbol in descr for symbol in [">", "<", "&", "'", "\""]):
        return "Found invalid symbols, please resubmit your suggestion!"
    if len(filename) > 60:
        return "Filename length is too long!"
    if not check_captcha(captcha_code):
        return "Invalid captcha. Try again."
    return "Admin will view your problem/suggestion very soon!"
