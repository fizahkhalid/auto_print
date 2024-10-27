import threading
from pynput import keyboard
import requests
import sys
import time

# Configuration
FASTAPI_URL = "http://localhost:8000/capture"

# Define hotkeys using CTRL + SHIFT + (1-7) for different timeframes
HOTKEYS = {
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('1')]): "1m",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('2')]): "5m",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('3')]): "15m",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('4')]): "1h",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('5')]): "4h",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('6')]): "1d",
    frozenset([keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('7')]): "1w",
}

current_keys = set()

def on_press(key):
    current_keys.add(key)
    for combo in HOTKEYS:
        if combo <= current_keys:
            timeframe = HOTKEYS[combo]
            capture_all_charts(timeframe)

def on_release(key):
    current_keys.discard(key)

def capture_all_charts(timeframe):
    url = f"{FASTAPI_URL}/{timeframe}"
    print(f"Sending request to capture all charts at {timeframe} timeframe. URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[SUCCESS] Screenshots for {timeframe} captured successfully.")
        else:
            print(f"[ERROR] Failed to capture screenshots for {timeframe}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"[EXCEPTION] Error capturing screenshots for {timeframe}: {str(e)}")

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    print("Hotkey listener started. Use CTRL + SHIFT + (1-7) to capture EUR and DXY charts:")
    print("1 = 1m, 2 = 5m, 3 = 15m, 4 = 1h, 5 = 4h, 6 = 1d, 7 = 1w")
    
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nHotkey listener stopped.")
        sys.exit()
