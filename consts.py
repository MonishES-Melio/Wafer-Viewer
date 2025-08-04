import pandas as pd

grid_csv = pd.read_csv("wafer_default.csv", header = None)

DEFAULT_GRID = grid_csv.values.flatten().tolist()

DEFAULT_CHIP_DATA = {}
for cell_id in DEFAULT_GRID:
    cell_id = int(cell_id)
    if cell_id != -1:
        chip_name = str(int(cell_id))
        DEFAULT_CHIP_DATA[cell_id] = {
            "chip_name": chip_name,
            "plot": None,  # Placeholder for generated plot
            "link": "https://melt-inspector.meliolabs.org/dashboard?dyeName=EVA&mouseBehaviour=click"
        }