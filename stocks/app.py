from flask import Flask, request, jsonify, render_template
import os
import logging
from dotenv import load_dotenv
import requests

load_dotenv("static/.env")

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")

@app.route("/stock", methods=["GET", "POST"])
def stock():
    api_key = os.getenv("API_KEY")
    if request.method == "POST":
        stock = request.form.get("symbol")
    elif request.method == "GET":
        stock = request.args.get("symbol")
    else:
        return jsonify({"error": "Invalid request method"}), 405
    if not stock:
        return jsonify({"error": "No stock symbol provided"}), 400
    api_url = f'https://api.api-ninjas.com/v1/stockprice?ticker={stock}'
    try:
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        response.raise_for_status()
        data = response.json()
        if "price" in data:
            return render_template("stock.html", name=stock.upper(), price=usd(data["price"]))
        else:
            return jsonify({"error": "Failed to retrieve stock data"}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve stock data"}), 500


def usd(value):
    return f"${value:,.2f}"

if __name__ == "__main__":
    app.run(debug=True)