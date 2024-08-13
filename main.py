import argparse
from src.web import check_citas
from src.utils import log_result, count_citas_found


def parse_args():
    # Initialize the command-line argument parser
    parser = argparse.ArgumentParser(description='Automate NIE submission.')
    
    # Define optional arguments
    parser.add_argument('--nie_code', type=str, required=True, help='NIE code to submit')
    parser.add_argument('--nombre_apellidos', type=str, required=True, help='Nombre y apellidos to submit')
    parser.add_argument('--office', type=str, required=True, help='Office to select')
    parser.add_argument('--tramite', type=str, required=True, help='Trámite to select')
    parser.add_argument('--citas_checked_count', type=int, help='Counter for citas', default=0)
    parser.add_argument('--telegram_token', type=str, help='Telegram bot token', default="")
    parser.add_argument('--telegram_chat_id', type=str, help='Telegram chat ID', default="")
    parser.add_argument('--telegram_send_message_offset', type=int, help='After <offset> checks, sends message to telegram', default=10)
    parser.add_argument('--sleep_after_check', type=int, help='Wait time after last cita check', default=300)
    
    args = parser.parse_args()
    return args


def main():
    # Parse the arguments
    args = parse_args()
    close_browser_tab = True
    citas = [False] * args.citas_checked_count

    while True:
        try:
            # Check for citas
            citas_available = check_citas(args, close_browser_tab)
            citas.append(citas_available)

            # Print if a cita is found and send a message to Telegram
            log_result(citas_available, args)

            # Count citas found and send statistics to Telegram
            count_citas_found(citas, args)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main()
