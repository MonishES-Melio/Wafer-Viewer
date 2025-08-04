# backend.py
from flask import Flask, jsonify, render_template_string, request, send_file
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import os
import copy
import tempfile
import logging
from consts import DEFAULT_GRID, DEFAULT_CHIP_DATA


MODE = os.environ.get("WAFER_MODE", "dev")

# The helper function is now imported directly from the new helper.py
from helper import get_plots_for_chip, get_chip_name

app = Flask(__name__, static_folder="static")

@app.route("/")
def serve_index():
    return render_template_string(open("wafer_viewer.html").read())

@app.route("/default-data")
def get_default_data():
    # Return a deep copy to avoid mutation
    return jsonify({
        "grid": copy.deepcopy(DEFAULT_GRID),
        "chip_data": copy.deepcopy(DEFAULT_CHIP_DATA)
    })

@app.route("/load-csv", methods=["POST"])
def load_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file)
        # Check for required columns
        if 'position' not in df.columns or 'chip_name' not in df.columns:
            return jsonify({"error": "CSV must contain 'position' and 'chip_name' columns."}), 400
        
        chip_data_from_csv = {}
        errors = [] # New: list to store errors
        for index, row in df.iterrows():
            position = int(row['position'])
            chip_name = row['chip_name']

            chip_name, error_message = get_chip_name(chip_name)
            if error_message:
                return jsonify({"error": error_message}), 400
            
            # Generate the plot and link for each chip
            plot_b64, error_message = get_plots_for_chip(chip_name)
            if error_message:
                errors.append(error_message)
                continue # New: skip the chip and continue with the loop
                
            link = f"https://melt-inspector.meliolabs.org/dashboard?dyeName=EVA&mouseBehaviour=click&chipName={chip_name}&advFilter=%5B%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_linear%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%2C%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_twin_parabolic%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%2C%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_isolated_parabolic%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%5D&activeFilter=%5Btrue%2Ctrue%2Ctrue%5D&advFilterColors=%5B%22%23ff1e05%22%2C%22%2300fa04%22%2C%22%235b66fb%22%5D"
            
            chip_data_from_csv[position] = {
                "chip_name": chip_name,
                "plot": plot_b64,
                "link": link
            }
        
        # Merge with existing chip_data or create new
        existing_grid = copy.deepcopy(DEFAULT_GRID)
        existing_chip_data = copy.deepcopy(DEFAULT_CHIP_DATA)
        existing_chip_data.update(chip_data_from_csv)
        
        return jsonify({
            "grid": existing_grid,
            "chip_data": existing_chip_data,
            "errors": errors # New: return the list of errors
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/load-data", methods=["POST"])
def load_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        data = pickle.load(file)
        grid = data.get("grid")
        chip_data = data.get("chip_data")
        return jsonify({"grid": grid, "chip_data": chip_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mode")
def get_mode():
    return jsonify({"mode": MODE})

# Only register /generate-chip in dev mode
if MODE == "dev":
    @app.route("/generate-chip", methods=["POST"])
    def generate_chip():
        data = request.get_json()
        cell_id = int(data.get("cell_id"))
        chip_name = data.get("chip_name")
        annotation = data.get("annotation")
        if not chip_name:
            return jsonify({"error": "chip_name required"}), 400
        
        chip_name, error_message = get_chip_name(chip_name)
        if error_message:
            return jsonify({"error": error_message}), 400
        
        plot_b64, error_message = get_plots_for_chip(chip_name)
        
        if error_message:
            return jsonify({"error": error_message}), 400
        
        link = f"https://melt-inspector.meliolabs.org/dashboard?dyeName=EVA&mouseBehaviour=click&chipName={chip_name}&advFilter=%5B%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_linear%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%2C%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_twin_parabolic%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%2C%5B%7B%22operator%22%3A%22AND%22%2C%22field%22%3A%22tp_isolated_parabolic%22%2C%22option%22%3A%5B%22True%22%5D%7D%5D%5D&activeFilter=%5Btrue%2Ctrue%2Ctrue%5D&advFilterColors=%5B%22%23ff1e05%22%2C%22%2300fa04%22%2C%22%235b66fb%22%5D"
        chip_data = {
            "chip_name": chip_name,
            "plot": plot_b64,
            "link": link,
            "annotation": annotation
        }
        return jsonify({"cell_id": cell_id, "chip_data": chip_data})

@app.route("/download-data", methods=["POST"])
def download_data():
    data = request.get_json()
    grid = data.get("grid")
    chip_data = data.get("chip_data")
    wafer_name = data.get("wafer_name", "wafer_data") # New: Get wafer name from request
    if grid is None or chip_data is None:
        return jsonify({"error": "Missing grid or chip_data"}), 400
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp:
        pickle.dump({"grid": grid, "chip_data": chip_data}, tmp)
        tmp.flush()
        tmp.seek(0)
        return send_file(
            tmp.name,
            as_attachment=True,
            download_name=f"{wafer_name}.pkl",
            mimetype="application/octet-stream"
        )

if __name__ == "__main__":
    app.run(debug=True)
