from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN
ASSET = "BTCUSD"
RISK_PERCENT = 0.10          # 10% del capital
TAKE_PROFIT_PERCENT = 0.015  # 1.5%
STOP_LOSS_PERCENT = 0.0075   # 0.75%

@app.route("/")
def home():
    return "Bot activo"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("Datos recibidos:", data)

    signal = data.get("signal", "").lower()
    price = float(data.get("price", 0))

    # CAPITAL VARIABLE
    capital = float(data.get("capital", 100))

    # MONTO AUTOMÁTICO
    amount = capital * RISK_PERCENT

    # VALIDACIONES
    if signal not in ["buy", "sell"]:
        print("⚠️ Señal inválida")
        return jsonify({"error": "Señal inválida"}), 400

    if price <= 0:
        print("⚠️ Precio inválido")
        return jsonify({"error": "Precio inválido"}), 400

    # CALCULAR TAKE PROFIT Y STOP LOSS
    if signal == "buy":

        take_profit = price * (1 + TAKE_PROFIT_PERCENT)
        stop_loss = price * (1 - STOP_LOSS_PERCENT)

    elif signal == "sell":

        take_profit = price * (1 - TAKE_PROFIT_PERCENT)
        stop_loss = price * (1 + STOP_LOSS_PERCENT)

    # DATOS DE OPERACIÓN
    trade = {
        "asset": ASSET,
        "signal": signal,
        "capital_actual": round(capital, 2),
        "monto_operacion": round(amount, 2),
        "precio_entrada": round(price, 2),
        "take_profit": round(take_profit, 2),
        "stop_loss": round(stop_loss, 2)
    }

    print("\n🚀 OPERACIÓN DETECTADA 🚀")
    print(trade)

    # AQUÍ DESPUÉS IRÁ LA CONEXIÓN REAL AL BROKER
    # abrir_operacion(trade)

    return jsonify({
        "status": "ok",
        "trade": trade
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
