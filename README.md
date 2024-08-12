# SpanishCita

Install dependencies and run
(do not forget to change NIE, NAME, SURNAME and other params if needed)

```(bash)
./install.sh
python3 main.py --nie_code="NIE" \
                --nombre_apellidos="NAME SURNAME" \
                --office="CNP MALLORCA GRANADOS, MALLORCA, 213" \
                --tramite="POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)" \
                --citas_found_count=0 \
                --telegram_token="" \
                --telegram_chat_id="" \
                --telegram_send_message_offset=10 \
                --sleep_after_check=600
```

only set `telegram-token`, `telegram-chat-id`, `telegram_send_message_offset` if you want to write messages to telegram
