# SpanishCita

Install dependencies and run
(do not forget to change NIE, NAME, SURNAME and other params if needed)

### 0. Download repo:
```(bash)
git clone https://github.com/Exdenta/SpanishCita.git
cd SpanishCita
```

### 1. Install dependencies
with conda:
```(bash)
./scripts/install_conda.sh
conda activate ./env
```

 with pip:
```(bash)
./scripts/install_pip.sh
```

### 2. Run
```(bash)
./run.sh
```
or
```(bash)
python3 main.py --nie_code="NIE" \
                --nombre_apellidos="NAME SURNAME" \
                --office="CNP MALLORCA GRANADOS, MALLORCA, 213" \
                --tramite="POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)" \
                --citas_checked_count=0 \
                --telegram_token="" \
                --telegram_chat_id="" \
                --telegram_send_message_offset=10 \
                --sleep_after_check=600
```

only set `telegram-token`, `telegram-chat-id`, `telegram_send_message_offset` if you want to write messages to telegram
