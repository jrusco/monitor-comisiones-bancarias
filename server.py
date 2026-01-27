"""
Backend server that exposes endpoints to trigger fee updater scripts.

Usage:
    # Development
    python server.py

    # Production
    gunicorn server:app

    Set API_KEY environment variable to require authentication:
        API_KEY=mysecret gunicorn server:app

Endpoints:
    POST /update/mercadopago  - Run Mercado Pago fee updater
    POST /update/bna          - Run BNA fee updater
    POST /update/bapro        - Run Banco Provincia fee updater
    POST /update/uala         - Run Ualá fee updater
    POST /update/all          - Run all updaters sequentially
    GET  /status              - Health check
"""

from flask import Flask, jsonify, request
import subprocess
import sys
import os
import logging
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

UPDATERS = {
    "mercadopago": "update_mercadopago_fee.py",
    "bna": "update_bna_fee.py",
    "bapro": "update_bapro_fee.py",
    "uala": "update_uala_fee.py",
}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# One lock per updater to prevent concurrent runs of the same script
_locks = {name: threading.Lock() for name in UPDATERS}


def require_api_key():
    """Returns an error response if API_KEY is set and the request doesn't match, else None."""
    if API_KEY is None:
        return None
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    if token != API_KEY:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    return None


def run_updater(name, script_name):
    script_path = os.path.join(PROJECT_DIR, script_name)
    if not os.path.isfile(script_path):
        return {"success": False, "error": f"Script not found: {script_name}"}, 404

    lock = _locks[name]
    if not lock.acquire(blocking=False):
        return {"success": False, "error": f"Updater '{name}' is already running"}, 409

    try:
        logger.info("Running updater: %s", script_name)
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
            timeout=120,
        )
        logger.info("Updater %s finished with code %d", script_name, result.returncode)

        return {
            "success": result.returncode == 0,
            "script": script_name,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }, 200 if result.returncode == 0 else 500

    except subprocess.TimeoutExpired:
        logger.error("Updater %s timed out", script_name)
        return {"success": False, "error": f"Script timed out: {script_name}"}, 504
    finally:
        lock.release()


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "updaters": list(UPDATERS.keys())})


@app.route("/update/<updater_name>", methods=["POST"])
def update(updater_name):
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    if updater_name not in UPDATERS:
        return jsonify({"success": False, "error": f"Unknown updater: {updater_name}"}), 404

    body, code = run_updater(updater_name, UPDATERS[updater_name])
    return jsonify(body), code


@app.route("/update/all", methods=["POST"])
def update_all():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    results = {}
    all_success = True
    for name, script in UPDATERS.items():
        body, _ = run_updater(name, script)
        results[name] = body
        if not body["success"]:
            all_success = False

    return jsonify({"success": all_success, "results": results}), 200 if all_success else 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
