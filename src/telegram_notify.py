import requests


def send_telegram_message(token: str, chat_id: str, message: str) -> None:
    print("send telegram message: " + message)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        print(f"Failed to send message: {response.text}")
