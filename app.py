from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    hostname = socket.gethostname()
    return f"Hello from Azure! Running on host: {hostname}"

if __name__ == "__main__":
    # Local run (pour tester avant de pousser sur Azure)
    app.run(host="0.0.0.0", port=8000)
