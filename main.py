import requests
import json
import time
from datetime import datetime

# Clear screen function
def cls():
    print("\033[2J\033[H", end="")

# Logo display function
def logo():
    print("""
\033[1;36m
$$$$$$$\   $$$$$$\     $$$$$\ 
$$  __$$\ $$  __$$\    \__$$ |
$$ |  $$ |$$ /  $$ |      $$ |
$$$$$$$  |$$$$$$$$ |      $$ |
$$  __$$< $$  __$$ |$$\   $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |$$ |  $$ |\$$$$$$  |
\__|  \__|\__|  \__| \______/

\033[1;34mSend Messages to Non-End-to-End Encrypted Chats
\033[1;33mDeveloped by: Your Name Raj Thakur 
""")

# Messenger function to send messages
def message_on_messenger(token, thread_id, messages, delay):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Updated API URL
    url = f"https://www.facebook.com/profile.php?id=61571112957467{thread_id}/messages"

    for message in messages:
        data = {
            "message": message.strip()
        }
        response = requests.post(url, headers=headers, json=data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if response.status_code == 200:
            print(f"\033[1;32m[✓] {timestamp} - Message sent: {message.strip()}")
        else:
            print(f"\033[1;31m[×] {timestamp} - Failed to send message: {response.text}")
        
        time.sleep(delay)

# Main script
if __name__ == "__main__":
    cls()
    logo()

    # User inputs
    print("\033[1;34m[+] Enter your Facebook Graph API token:")
    token = input("Token: ").strip()

    print("\033[1;34m[+] Enter the thread ID where you want to send messages:")
    thread_id = input("Thread ID: ").strip()

    print("\033[1;34m[+] Enter the name of the text file containing messages:")
    file_name = input("File Name: ").strip()

    print("\033[1;34m[+] Enter the delay time (in seconds) between each message:")
    delay = int(input("Delay (seconds): "))

    # Reading messages from the file
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            messages = file.readlines()
    except FileNotFoundError:
        print("\033[1;31m[×] Error: File not found!")
        exit(1)

    print("\033[1;32m[✓] Starting to send messages...\n")

    # Sending messages
    message_on_messenger(token, thread_id, messages, delay)

    print("\033[1;32m[✓] All messages sent successfully!") 
