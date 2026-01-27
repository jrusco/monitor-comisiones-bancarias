"""
Backend server that exposes endpoints to trigger fee updater scripts.

Usage:
    python server.py
    # Server runs on http://localhost:5000

Endpoints:
    POST /update/mercadopago  - Run Mercado Pago fee updater
    POST /update/bna          - Run BNA fee updater
    POST /update/bapro        - Run Banco Provincia fee updater
    POST /update/uala         - Run Ualá fee updater
    POST /update/all          - Run all updaters sequentially
    GET  /status              - Health check
"""

from flask import Flask, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

UPDATERS = {
    "mercadopago": "update_mercadopago_fee.py",
    "bna": "update_bna_fee.py",
    "bapro": "update_bapro_fee.py",
    "uala": "update_uala_fee.py",
}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_updater(script_name):
    script_path = os.path.join(PROJECT_DIR, script_name)
    if not os.path.isfile(script_path):
        return {"success": False, "error": f"Script not found: {script_name}"}, 404

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        timeout=120,
    )

    return {
        "success": result.returncode == 0,
        "script": script_name,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }, 200 if result.returncode == 0 else 500


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "updaters": list(UPDATERS.keys())})


@app.route("/update/<updater_name>", methods=["POST"])
def update(updater_name):
    if updater_name not in UPDATERS:
        return jsonify({"success": False, "error": f"Unknown updater: {updater_name}"}), 404

    body, code = run_updater(UPDATERS[updater_name])
    return jsonify(body), code


@app.route("/update/all", methods=["POST"])
def update_all():
    results = {}
    all_success = True
    for name, script in UPDATERS.items():
        body, _ = run_updater(script)
        results[name] = body
        if not body["success"]:
            all_success = False

    return jsonify({"success": all_success, "results": results}), 200 if all_success else 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
