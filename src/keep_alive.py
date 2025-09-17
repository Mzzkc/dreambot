from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Status</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: rgba(0,0,0,0.3);
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { margin: 0 0 20px 0; }
            .status {
                display: inline-block;
                padding: 10px 20px;
                background: #4CAF50;
                border-radius: 50px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐉 Ahamkara Bot</h1>
            <div class="status">✅ ONLINE</div>
            <p>The wish-dragon stirs in the digital realm...</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()