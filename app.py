from flask import Flask, render_template
import os
from flask_cloudflared import run_with_cloudflared

app = Flask(__name__)
run_with_cloudflared(app) # يفتح لج الرابط العالمي

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open_notepad')
def open_notepad():
    os.system("notepad.exe")
    return "تم فتح Notepad"

@app.route('/open_chrome')
def open_chrome():
    os.system("start chrome")
    return "تم فتح Chrome"

if __name__ == '__main__':
    app.run()