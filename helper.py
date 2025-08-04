import pandas as pd
import io
import logging
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from melt_data_layer import DAL, DALConfig
from melt_data_layer.constants import *
dal_config = DALConfig()
dal = DAL(dal_config)

def get_chip_name(chip_name):
    try:
        chips_in_well_meta_db = dal.get_local_runs_id_from_db(
            regex=chip_name, lookup_db=WELL_META_DB
        )
        if not chips_in_well_meta_db:
            return None, f"Chip {chip_name} not found in well meta database."
        
        chip = chips_in_well_meta_db[0]
        return chip, None
    except Exception as e:
        return None, f"No Chip Name found for {chip_name}: {e}"


def extract_annotations_df(chip_name , dal):
    try:
        well_metadata = dal.get_well_meta_data(chip_name)
        well_metadata_df = pd.DataFrame(well_metadata)
        
        # Check for required columns
        required_cols = ["tp_linear", "tp_twin_parabolic", "tp_isolated_parabolic"]
        if not all(col in well_metadata_df.columns for col in required_cols):
            return None, f"Latest annotations not available for the chip {chip_name}."

        return well_metadata_df, None
    except Exception as e:
        return None, f"Extracting annotations failed for chip {chip_name}: {e}"

def extract_spatial_df(chip_name, dal):
    chips_in_signal_well_db = dal.get_local_runs_id_from_db(chip_name, SIGNAL_MELT_DB)
    chip = chips_in_signal_well_db[0]
    well = dal.get_signal_well_data(chip)

    df_temp = pd.DataFrame()
    column_names = []
    data = []
    x = []
    y = []
    flag = ""
    if "radius" in well[0]:
        radius = []
        flag = "QS"
    elif ("w" in well[0] and "h" in well[0]):
        w = []
        h = []
        angle = []
        flag = "BLIND"
    val = []
    for i in range(0, len(well)):
        x_coord = well[i].get("cx", well[i].get("x"))
        y_coord = well[i].get("cy", well[i].get("y"))

        if flag == "QS":
            radius.append(well[i].get("radius"))
        elif flag == "BLIND":
            w.append(well[i].get("w"))
            h.append(well[i].get("h"))
            angle.append(well[i].get("angle"))
        
        if x_coord is not None and y_coord is not None:
            x.append(x_coord)
            y.append(y_coord)
        else:
            print(f"Warning: Missing coordinates at index {i}")

    df_temp["cx"] = x
    df_temp["cy"] = y
    if(flag == "QS"):
        df_temp["radius"] = radius
    elif(flag == "BLIND"):
        df_temp["w"] = w
        df_temp["h"] = h
        df_temp["angle"] = angle

    return df_temp

def get_plots_for_chip(chip_name):
    """
    Generates a mock plot for a given chip.
    This function replaces the original implementation and avoids the problematic dependency.
    It now includes a try-except block for robust error handling.
    """
    try:
        original_annotations, error_message = extract_annotations_df(chip_name, dal)
        if error_message:
            return None, error_message
        
        spatial_data  = extract_spatial_df(chip_name, dal)
        if spatial_data is None:
            return None, f"Failed to extract spatial data for chip {chip_name}."

        # Add annotation data to spatial_data, checking for key existence
        spatial_data["tp_linear"] = original_annotations["tp_linear"].copy()
        spatial_data["tp_twin_parabolic"] = original_annotations["tp_twin_parabolic"].copy()
        spatial_data["tp_isolated_parabolic"] = original_annotations["tp_isolated_parabolic"].copy()
        
        def get_tp_type(row):
            if row["tp_linear"]:
                return "tp_linear"
            elif row["tp_twin_parabolic"]:
                return "tp_twin_parabolic"
            elif row["tp_isolated_parabolic"]:
                return "tp_isolated_parabolic"
            else:
                return "negative"
        
        spatial_data["tp_type"] = spatial_data.apply(get_tp_type, axis=1)
        color_dict = {
            "negative": 'black',
            "tp_linear": '#00FFFF',         
            "tp_twin_parabolic": '#FF00FF', 
            "tp_isolated_parabolic": '#39FF14'
        }
        fig, ax = plt.subplots(figsize=(10, 10))
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        for _, row in spatial_data.iterrows():
            color = color_dict.get(row["tp_type"], 'white')
            rect = plt.Rectangle(
                (row["cx"] - row["w"]/2, row["cy"] - row["h"]/2),
                row["w"],
                row["h"],
                color=color,
                alpha=0.8,
                linewidth=0,
            )
            ax.add_patch(rect)
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=color_dict[k], edgecolor='none', label=k)
            for k in color_dict
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.margins(0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        plot_b64 = base64.b64encode(buf.read()).decode('utf-8')
        return plot_b64, None
    except Exception as e:
        # Catch any exceptions during plot generation and return a specific error.
        return None, f"Plot generation failed for chip {chip_name}: {e}"

