from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# CONFIGURACIÓN GENERAL
# =========================

SYMBOL = "BTCUSDT"

RISK_PERCENT = 0.10          # Usa el 10% del capital
TAKE_PROFIT_PERCENT = 0.015  # Take Profit: 1.5%
STOP_LOSS_PERCENT = 0.0075   # Stop Loss: 0.75%

MIN_CAPITAL = 10             # Capital mínimo permitido
MAX_RISK_PERCENT = 0.10      # Máximo 10% por operación


@app.route("/")
def home():
    return "Bot activo para trading normal BTCUSDT"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json

        print("\n📩 DATOS RECIBIDOS:")
        print(data)

        # =========================
        # RECIBIR DATOS DEL WEBHOOK
        # =========================

        signal = str(data.get("signal", "")).lower()
        price = float(data.get("price", 0))
        capital = float(data.get("capital", 0))

        # =========================
        # VALIDACIONES
        # =========================

        if signal not in ["buy", "sell"]:
            return jsonify({
                "status": "error",
                "message": "Señal inválida. Usa buy o sell."
            }), 400

        if price <= 0:
            return jsonify({
                "status": "error",
                "message": "Precio inválido."
            }), 400

        if capital < MIN_CAPITAL:
            return jsonify({
                "status": "error",
                "message": "Capital insuficiente."
            }), 400

        # =========================
        # CALCULAR MONTO
        # =========================

        risk_percent = min(RISK_PERCENT, MAX_RISK_PERCENT)
        amount_usdt = capital * risk_percent

        # Cantidad aproximada de BTC a comprar/vender
        quantity_btc = amount_usdt / price

        # =========================
        # CALCULAR TP Y SL
        # =========================

        if signal == "buy":
            side = "LONG"
            take_profit = price * (1 + TAKE_PROFIT_PERCENT)
            stop_loss = price * (1 - STOP_LOSS_PERCENT)

        else:
            side = "SHORT"
            take_profit = price * (1 - TAKE_PROFIT_PERCENT)
            stop_loss = price * (1 + STOP_LOSS_PERCENT)

        trade = {
            "symbol": SYMBOL,
            "signal": signal,
            "side": side,
            "capital_actual": round(capital, 2),
            "porcentaje_usado": f"{risk_percent * 100}%",
            "monto_operacion_usdt": round(amount_usdt, 2),
            "cantidad_btc": round(quantity_btc, 8),
            "precio_entrada": round(price, 2),
            "take_profit": round(take_profit, 2),
            "stop_loss": round(stop_loss, 2)
        }

        print("\n🚀 OPERACIÓN CALCULADA:")
        print(trade)

        # =========================
        # AQUÍ IRÁ LA CONEXIÓN REAL AL BROKER
        # =========================
        # ejecutar_operacion(trade)

        return jsonify({
            "status": "ok",
            "message": "Operación calculada correctamente",
            "trade": trade
        }), 200

    except Exception as e:
        print("❌ ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================
# FUNCIÓN FUTURA PARA BROKER
# =========================

def ejecutar_operacion(trade):
    """
    Aquí después conectamos Binance, Bybit, OKX, Bitget, etc.

    Esta función debería:
    1. Abrir operación LONG o SHORT.
    2. Colocar Take Profit.
    3. Colocar Stop Loss.
    4. Guardar registro de la operación.
    """

    print("Conexión al broker pendiente.")
    print(trade)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
