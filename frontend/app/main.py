from dotenv import load_dotenv

from flask_cors import CORS  # type: ignore
from flask import Flask, render_template, request, jsonify

import os
import socket
import requests
import datetime

import numpy as np
import plotly.io as pio  # type: ignore
import plotly.graph_objs as go  # type: ignore

load_dotenv()

# Get the port from the environment variable
BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS")
BACKEND_PORT = os.getenv("BACKEND_PORT")

PORT = int(os.getenv("FRONTEND_PORT", 3000))
HOST = os.getenv("FRONTEND_ADDRESS", "0.0.0.0")

FRONTEND_VERSION = os.getenv("FRONTEND_VERSION", "1.0.0")

app = Flask(__name__)


def is_ip_address(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

if is_ip_address(BACKEND_ADDRESS):
    print(f"BACKEND_ADDRESS is an IP address: {BACKEND_ADDRESS}")
    BACKEND_IP = BACKEND_ADDRESS
else:
    print(f"BACKEND_ADDRESS is a hostname: {BACKEND_ADDRESS}")
    try:
        BACKEND_IP = socket.gethostbyname(BACKEND_ADDRESS)
        print(f"Backend IP: {BACKEND_IP}")
    except socket.gaierror:
        BACKEND_IP = BACKEND_ADDRESS

PLOUF_BACKEND_URL = f"http://{BACKEND_IP}:{BACKEND_PORT}"

CORS(app, resources={r"/*": {"origins": "*"}})


# Routes
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/pools")
def pools():
    response = requests.get(f"{PLOUF_BACKEND_URL}/pool/all")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template("pools.html", data=response.json(), today=today)


@app.route("/pool/<pool_id>")
def pool(pool_id):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"{PLOUF_BACKEND_URL}/pool/{pool_id}")
    response = response.json()
    logbook = response["pool"]["logbook"]
    logbook = sorted(logbook, key=lambda x: x["date"])
    chlorine_data = [log["chlorine_level"] for log in logbook]
    ph_data = [log["pH_level"] for log in logbook]
    dates = [log["date"] for log in logbook]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(len(chlorine_data)),
            y=chlorine_data,
            mode="lines",
            name="Chlorine level",
        )
    )
    fig.add_trace(
        go.Scatter(x=np.arange(len(ph_data)), y=ph_data, mode="lines", name="pH level")
    )
    fig.update_xaxes(tickvals=np.arange(len(dates)), ticktext=dates)
    fig.update_layout(title="Pool logbook", xaxis_title="Time", yaxis_title="Value")

    graph_html = pio.to_html(fig, full_html=False)

    return render_template(
        "pool_details.html",
        data=response,
        pool_id=pool_id,
        graph_html=graph_html,
        today=today,
    )


@app.route("/pool/<pool_id>/update")
def pool_update(pool_id):
    response = requests.get(f"{PLOUF_BACKEND_URL}/pool/{pool_id}")
    response = response.json()
    pool_data = response["pool"]
    return render_template("update_pool.html", data=pool_data, pool_id=pool_id)


@app.route("/pool/<pool_id>/log/<log_id>/update")
def log_update(pool_id, log_id):
    response = requests.get(f"{PLOUF_BACKEND_URL}/pool/{pool_id}/log/{log_id}")
    response = response.json()
    log_data = response["log"]
    return render_template(
        "update_log.html", data=log_data, pool_id=pool_id, log_id=log_id
    )


@app.route("/health")
def health():
    api_response = requests.get(f"{PLOUF_BACKEND_URL}/health/api/uptime")
    mongodb_response = requests.get(f"{PLOUF_BACKEND_URL}/health/mongo/full_health")
    return render_template(
        "health.html", api=api_response.json(), mongo=mongodb_response.json()
    )


# Local API routes
@app.route("/add-pool", methods=["POST"])
def add_pool():
    pool_data = request.get_json()
    backend_url = f"{PLOUF_BACKEND_URL}/pool"
    try:
        response = requests.post(backend_url, json=pool_data)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete-pool/<pool_id>", methods=["DELETE"])
def delete_pool(pool_id):
    backend_url = f"{PLOUF_BACKEND_URL}/pool/{pool_id}"
    try:
        response = requests.delete(backend_url)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update-pool/<pool_id>", methods=["PUT"])
def update_pool(pool_id):
    pool_data = request.get_json()
    backend_url = f"{PLOUF_BACKEND_URL}/pool/{pool_id}"
    try:
        response = requests.put(backend_url, json=pool_data)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add-log/<pool_id>", methods=["POST"])
def add_log(pool_id):
    log_data = request.get_json()
    backend_url = f"{PLOUF_BACKEND_URL}/pool/{pool_id}/log"
    try:
        response = requests.post(backend_url, json=log_data)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update-log/<pool_id>/<log_id>", methods=["PUT"])
def update_log(pool_id, log_id):
    log_data = request.get_json()
    backend_url = f"{PLOUF_BACKEND_URL}/pool/{pool_id}/log/{log_id}"
    try:
        response = requests.put(backend_url, json=log_data)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete-log/<pool_id>/<log_id>", methods=["DELETE"])
def delete_log(pool_id, log_id):
    backend_url = f"{PLOUF_BACKEND_URL}/pool/{pool_id}/log/{log_id}"
    try:
        response = requests.delete(backend_url)
        response.raise_for_status()  # Check for errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Frontend version: {FRONTEND_VERSION}")
    app.run(debug=True, host=HOST, port=PORT)
