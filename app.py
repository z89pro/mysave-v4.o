import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is Running | Powered by Zain"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
