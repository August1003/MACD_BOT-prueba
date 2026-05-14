from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("Datos recibidos:", data)

    signal = data.get("signal")

    if signal == "buy":
        print("🟢 SEÑAL DE COMPRA")

    elif signal == "sell":
        print("🔴 SEÑAL DE VENTA")

    else:
        print("⚠️ Señal desconocida")

    return {"status": "ok"}, 200
