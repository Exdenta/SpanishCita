from .telegram_notify import send_telegram_message
from .find_queue_number import find_queue_number


def log_result(citas_available: bool, args):
    if citas_available:
        message = "Citas available"
        print(message)
        if args.telegram_token != "":
            send_telegram_message(args.telegram_token, args.telegram_chat_id, message)
        else:
            message = "Citas not found"
            print(message)


def count_citas_found(args):
    global citas
    if not citas:
        citas = [False] * args.citas_checked_count
    
    citas.append(args.citas_available)
    if len(citas) % args.telegram_send_message_offset == 0:
        queue_number = find_queue_number(args.office, args.tramite)
        found_citas = citas.count(True)
        message = f"Statistics: checked {len(citas)}, found {found_citas}. Current queue number: {queue_number}"
        print(message)
        if args.telegram_token != "":
            send_telegram_message(args.telegram_token, args.telegram_chat_id, message)
