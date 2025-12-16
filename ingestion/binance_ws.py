import json
import threading
from datetime import datetime
from websocket import WebSocketApp

from storage.db import insert_tick


BINANCE_WS_BASE = "wss://fstream.binance.com/ws"


def on_message(ws, message):
    
    try:
        data = json.loads(message)

        if data.get("e") != "trade":
            return

        symbol = data["s"].lower()
        price = float(data["p"])
        quantity = float(data["q"])

        event_time = datetime.utcfromtimestamp(
            data["T"] / 1000
        ).isoformat()

        insert_tick(
            symbol=symbol,
            timestamp=event_time,
            price=price,
            quantity=quantity
        )

    except Exception as e:
        print(f"[ERROR] Failed to process message: {e}")


def on_error(ws, error):
    print(f"[ERROR] WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"[INFO] WebSocket closed: {close_status_code} - {close_msg}")


def on_open(ws):
    print("[INFO] WebSocket connection opened")


def start_symbol_stream(symbol: str):
    """
    Start a WebSocket stream for a single symbol.
    """
    url = f"{BINANCE_WS_BASE}/{symbol}@trade"

    ws = WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()


def start_ingestion(symbols):
    
    threads = []

    for symbol in symbols:
        t = threading.Thread(
            target=start_symbol_stream,
            args=(symbol,),
            daemon=True
        )
        t.start()
        threads.append(t)

    return threads
