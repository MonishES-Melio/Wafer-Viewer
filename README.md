Wafer Viewer
Overview
Wafer Viewer is a web-based tool for visualizing semiconductor wafer data. It provides an interactive 10x10 grid that maps individual chips on a wafer, allowing users to view plots, manage multiple wafers, and dynamically load data from various sources. The application is built with a Python Flask backend and a vanilla JavaScript frontend.

Features
Interactive Wafer Grid: A 10x10 grid visually represents the wafer, with distinct styles for active, inactive, and data-populated cells.

Multi-Wafer Management:

Add, rename, and delete multiple wafers in a single session.

Seamlessly switch between different wafers via a sidebar.

Dynamic Data Loading:

Load from CSV: Upload a .csv file with position and chip_name columns to populate the grid. The backend fetches data and generates plots on the fly.

Load from .pkl: Load a previously saved wafer session from a .pkl file.

Chip Interaction:

View Plot: Click on a chip to open its detailed plot in a new tab.

External Link: Access a detailed external dashboard for each chip via a link icon.

Show/Hide Chip: Toggle the visibility of individual chips using an eye icon to focus on specific areas of the wafer.

Error Handling:

If a chip fails to load from a CSV, a notification appears, and the process continues without halting.

Reliable backend logging for easier debugging.

Developer Mode: An optional dev mode unlocks advanced features:

On-the-Fly Chip Generation: Click any active cell to manually input a chip name and generate its plot.

Download Data: Save the current state of any wafer to a .pkl file.

Installation
Follow these instructions to set up and run the Wafer Viewer on your local machine.

Prerequisites
Python 3.11+

pip (Python package installer)

1. Clone the Repository
git clone <your-repository-url>
cd <your-repository-directory>

2. Set Up a Virtual Environment (Recommended)
## Create a virtual environment
```
python -m venv venv
```

## Activate the virtual environment
## On Windows
```
venv\Scripts\activate
```
## On macOS/Linux
```
source venv/bin/activate
```

3. Create requirements.txt
Create a file named requirements.txt in the root of your project directory and add the following dependencies:

Flask
pandas
matplotlib
numpy
seaborn
melt_data_layer


4. Install Dependencies
Install all the required packages using pip:
```
pip install -r requirements.txt
```
Running the Application
Standard Mode
To run the application in standard user mode, simply execute the backend.py script:
```
python backend.py
```
The application will be available at http://127.0.0.1:5000.

Developer Mode
To enable developer mode and unlock advanced features, set the WAFER_MODE environment variable to dev before running the application.

On macOS/Linux:
```
export WAFER_MODE=dev
python backend.py
```
On Windows (Command Prompt):
```
set WAFER_MODE=dev
python backend.py
```
On Windows (PowerShell):
```
$env:WAFER_MODE="dev"
python backend.py
```
You will now see additional buttons in the UI for generating chips and downloading wafer data. Logs in the terminal will also be more verbose.
