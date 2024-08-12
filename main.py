import argparse
import time
from web import check_citas
from telegram_notify import send_telegram_message
from find_queue_number import find_queue_number

def parse_args():
    # Initialize the command-line argument parser
    parser = argparse.ArgumentParser(description='Automate NIE submission.')
    parser.add_argument('nie_code', type=str, help='NIE code to submit')
    parser.add_argument('nombre_apellidos', type=str, help='Nombre y apellidos to submit')
    parser.add_argument('office', type=str, help='Office to select')
    parser.add_argument('tramite', type=str, help='Trámite to select')
    parser.add_argument('telegram_token', type=str, help='Telegram bot token')
    parser.add_argument('telegram_chat_id', type=str, help='Telegram chat ID')
    args = parser.parse_args()
    return args

def main():
    # Parse the arguments
    args = parse_args()
    nie_code = args.nie_code
    nombre_apellidos = args.nombre_apellidos
    office = args.office
    tramite = args.tramite
    telegram_token = args.telegram_token
    telegram_chat_id = args.telegram_chat_id

    citas = [False] * 1339
    # Check for citas
    while True:
        try:
            citas_available = check_citas(nie_code, nombre_apellidos, office, tramite, False, 250)
            if citas_available:
                message = "Citas available"
                print(message)
                send_telegram_message(telegram_token, telegram_chat_id, message)
            else:
                message = "-"
                print(message)
                # send_telegram_message(telegram_token, telegram_chat_id, message)
            citas.append(citas_available)
            if len(citas) % 10 == 0:
                queue_number = find_queue_number(office, tramite)
                found_citas = citas.count(True)
                message = f"Statistics: checked {len(citas)}, found {found_citas}. Current queue number: {queue_number}"
                print(message)
                send_telegram_message(telegram_token, telegram_chat_id, message)
            time.sleep(300)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()
