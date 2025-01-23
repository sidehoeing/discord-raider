import colorama
from colorama import Fore
import os
import socket
import requests
import threading
import time
import secrets
import string
import sys

mag = Fore.LIGHTMAGENTA_EX
blue = Fore.LIGHTBLUE_EX
yel = Fore.LIGHTYELLOW_EX
red = Fore.LIGHTRED_EX
gre = Fore.LIGHTGREEN_EX
res = Fore.RESET

question = f"- [{blue}?{res}]"
warning = f"- [{yel}!{res}]"
success = f"- [{gre}+{res}]"
error = f"- [{red}-{res}]"

desktop_name = socket.gethostname()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_version(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"{warning} Failed to fetch version. Status code: {response.status_code}")
            return "Unknown"
    except requests.RequestException as e:
        print(f"{error} Error fetching version: {e}")
        return "Unknown"

clear_screen()

version_url = "https://raw.githubusercontent.com/sidehoeing/discord-raider/refs/heads/main/version.txt"
version = fetch_version(version_url)
banner = f"""{blue}

                            ██▀███   ▄▄▄       ██▓▓█████▄      ▓██   ██▓ ▒█████   █    ██ 
                           ▓██ ▒ ██▒▒████▄    ▓██▒▒██▀ ██▌      ▒██  ██▒▒██▒  ██▒ ██  ▓██▒
                           ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒░██   █▌       ▒██ ██░▒██░  ██▒▓██  ▒██░
                           ▒██▀▀█▄  ░██▄▄▄▄██ ░██░░▓█▄   ▌       ░ ▐██▓░▒██   ██░▓▓█  ░██░
                           ░██▓ ▒██▒ ▓█   ▓██▒░██░░▒████▓  ██▓   ░ ██▒▓░░ ████▓▒░▒▒█████▓ 
                           ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▓   ▒▒▓  ▒  ▒▓▒    ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ 
                             ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░ ░ ▒  ▒  ░▒   ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░ 
                             ░░   ░   ░   ▒    ▒ ░ ░ ░  ░  ░    ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░ 
                              ░           ░  ░ ░     ░      ░   ░ ░         ░ ░     ░     
                                                  ░        ░   ░ ░                       
\n{res}Welcome to raid.you {desktop_name}, you are currently using {version}.                       
"""

print(f"{banner}{res}")

def validate_tokens(tokens):
    valid_tokens = []
    for token in tokens:
        url = "https://discord.com/api/v9/users/@me"
        headers = {"Authorization": token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"{success} Token {token[:25]}... is valid!")
            valid_tokens.append(token)
        else:
            print(f"{error} Token {token[:25]}... is invalid!")
    return valid_tokens

def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def load_emojis(file_path="emojis.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            emojis = [line.strip() for line in file if line.strip()]
        if emojis:
            print(f"{success} Loaded {len(emojis)} emojis.")
        else:
            print(f"{error} No emojis found in {file_path}.")
        return emojis
    except FileNotFoundError:
        print(f"{error} emojis.txt not found!")
        return []

def generate_random_emojis(emojis, count=5):
    return ''.join(secrets.choice(emojis) for _ in range(count)) if emojis else ""

def send_message(token, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {"content": message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"{success} Message sent successfully with token {token[:25]}...")
    else:
        print(f"{error} Failed to send message with token {token[:25]}... (Status: {response.status_code})")

def spam_with_tokens(tokens, channel_id, message, include_random_string, include_random_emojis, emojis, message_count):
    def thread_task(token):
        for _ in range(message_count):
            final_message = message
            if include_random_string:
                final_message += " " + generate_random_string()
            if include_random_emojis:
                final_message += " " + generate_random_emojis(emojis)
            send_message(token, channel_id, final_message)

    threads = []
    for token in tokens:
        t = threading.Thread(target=thread_task, args=(token,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def load_tokens(file_path="tokens.txt"):
    try:
        with open(file_path, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
        if tokens:
            print(f"{success} Loaded {len(tokens)} tokens.")
        else:
            print(f"{error} No tokens found in {file_path}.")
        return tokens
    except FileNotFoundError:
        print(f"{error} tokens.txt not found! {warning} Closing in 5 seconds.")
        return []

def restart_script():
    print(f"{warning} Restarting the script...")
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    tokens = load_tokens()
    emojis = load_emojis()

    if tokens:
        valid_tokens = validate_tokens(tokens)
        if valid_tokens:
            channel_id = input(f"{question} Enter the channel ID: ")
            message = input(f"{question} Enter the message to send: ")
            try:
                message_count = int(input(f"{question} Enter the number of messages to send: "))
                if message_count > 9999:
                    print(f"{warning} Message count exceeds 9999. Sending messages infinitely...")
                    message_count = float('inf')
            except ValueError:
                print(f"{error} Invalid input! Defaulting to 1 message.")
                message_count = 1

            include_random_string = input(f"{question} Include a random string after the message? (yes/no): ").strip().lower() == "yes"
            include_random_emojis = input(f"{question} Include random emojis after the message? (yes/no): ").strip().lower() == "yes"

            spam_with_tokens(valid_tokens, channel_id, message, include_random_string, include_random_emojis, emojis, message_count)

            restart_script()
        else:
            print(f"{error} No valid tokens to proceed.")
    else:
        print(f"{warning} No tokens to load. Exiting.")
