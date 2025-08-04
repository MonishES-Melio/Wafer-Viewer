Wafer Viewer User Guide
1. Introduction
Welcome to the Wafer Viewer! This guide will walk you through all the features of the application, from managing wafers to interacting with individual chips.

The main interface is divided into two sections: the Sidebar on the left for managing your wafers, and the Main Content Area on the right where you view and interact with the wafer grid.

2. The Main Interface
Sidebar
The sidebar is your mission control for handling different wafers.

Add Wafer Button: Click this to create a new, empty wafer. You will be prompted to give it a name.

Wafer List: All wafers you have added or loaded will appear in a list here. The currently active wafer is highlighted in blue.

Main Content Area
Controls Bar: A set of buttons at the top right allows you to perform actions on the currently active wafer.

Wafer Name: The name of the currently active wafer is displayed prominently as a title.

Wafer Grid: The 10x10 grid is a visual representation of the wafer.

3. Core Features & How to Use Them
Managing Wafers
Adding a Wafer: Click the Add Wafer button in the sidebar. Enter a unique name when prompted.

Switching Wafers: Simply click on any wafer's name in the sidebar list to make it the active one. The grid will update instantly.

Renaming a Wafer: Hover over a wafer in the sidebar and click the pencil icon. The name will become an editable text field. Type the new name and press Enter or click away to save.

Deleting a Wafer: Hover over a wafer and click the trash can icon. A confirmation pop-up will appear to prevent accidental deletion.

Loading Data into the Grid
Load from CSV:

Click the Load CSV button (only visible in dev mode).

Select a .csv file. The file must contain two columns: position (the cell number, 1-100) and chip_name.

The application will read the file, fetch the data for each chip, generate a plot, and place it in the correct cell.

If any chip fails to load, a yellow warning notification will pop up for each failure, but the process will continue for the remaining chips.

Load from .pkl File:

Click the Load Data button.

Select a .pkl file that was previously saved from this tool.

This will load the entire wafer, including all chip plots and their hidden/shown states, into a new tab in the sidebar.

Clear Wafer:

Click the Clear button.

This will remove all chip data from the currently active wafer, resetting it to a blank state.

Interacting with the Grid
Cell States:

Dark Gray: An inactive cell.

Light Blue: An active but empty cell, ready for data.

Plot Image: An active cell with chip data.

View Full Plot: Click anywhere on a cell containing a plot to open a larger version of the plot and its metadata in a new browser tab.

External Dashboard Link: Click the link icon in the top-left corner of a cell to open its associated external dashboard.

Show/Hide a Chip:

Click the eye icon in the top-right corner of a cell.

A dark shade will cover the cell, visually "hiding" it so you can focus on other chips. The main click functionality is disabled while hidden.

Click the slashed-eye icon to "unhide" the cell, returning it to normal.

4. Developer Mode Features
To access these features, you must run the application in dev mode (see installation instructions).

Generate a Single Chip:

In dev mode, click on any active, empty (light blue) cell.

A modal will appear asking for a Chip Name and an optional Annotation.

After submitting, the backend will generate the plot and place it in the selected cell.

Download Wafer Data:

Click the Download Data button.

This will save the current state of the active wafer, including all its chip data and hidden states, into a .pkl file.

This file can be loaded back into the application later using the Load Data button.