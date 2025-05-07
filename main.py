from flask import Flask, request, jsonify
from scraper import scrape_bifimed

app = Flask(__name__)

@app.route("/bifimed", methods=["GET"])
def consultar_bifimed():
    principio_activo = request.args.get("q", "")
    if not principio_activo:
        return jsonify({"error": "Debes proporcionar un principio activo con ?q="}), 400

    resultados = scrape_bifimed(principio_activo)
    return jsonify(resultados)
