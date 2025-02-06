from flask import Flask, render_template, request, jsonify
import logging
import os
from dotenv import load_dotenv

load_dotenv("static/api.env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        stock_name = request.form.get("symbol")
    else:
        stock_name = request.args.get("symbol")
    if not stock_name:
        return jsonify({"error": "Stock symbol is required"}), 400
    return render_template("search.html", name=stock_name)

@app.route("/stock", methods=["GET"])
def stock():
    try:
        stock_name = request.args.get("symbol")
        if not stock_name:
            return jsonify({"error": "Stock symbol is required"}), 400
        api_key = os.getenv("API_KEY")
        return render_template("stock.html", name=stock_name, api_key=api_key)
    
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "An error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", False))
