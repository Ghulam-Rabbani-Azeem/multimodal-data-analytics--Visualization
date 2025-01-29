# Multimodal Data Visualization Dashboard

## Description

This project provides an interactive data dashboard built using **Python**, **Dash**, and **Plotly**. The dashboard allows you to visualize data across different plot types, such as cluster maps, heatmaps, histograms, and correlation matrices. It has been designed with the intention of helping students learn how to build and work with data visualization dashboards in Python.

The primary objective of this project is to show how we can create intuitive and dynamic dashboards that display various types of data and allow interaction. It is beginner-friendly, and we provide easy-to-understand explanations of the code to ensure students can grasp the core concepts of interactive plotting and data visualization.

### Features:
- **Cluster Map**: Visualizes clusters of "persons" and "vehicles" across locations.
- **Heatmap**: Shows the relationship between different metrics like "greeness" and "noise" across geographic locations.
- **Histogram**: Allows users to explore the distribution of numerical features within the dataset.
- **Correlation Matrix**: Visualizes the correlation between features for a selected place.

By the end of this tutorial, you'll be able to:
- Build a fully functional interactive dashboard using Dash and Plotly.
- Generate various types of plots including heatmaps, histograms, scatter maps, and correlation analysis.
- Understand how callbacks are used in Dash to make the dashboard interactive and update in real time.

## Table of Contents
1. [Introduction](#introduction)
2. [Install Required Libraries](#install-required-libraries)
3. [Project Structure](#project-structure)
4. [Understanding the Code](#understanding-the-code)
   - [Step 1: Import Required Libraries](#step-1-import-required-libraries)
   - [Step 2: Initialize the Dash Application](#step-2-initialize-the-dash-application)
   - [Step 3: Load Your Processed Data](#step-3-load-your-processed-data)
   - [Step 4: Normalize Data Columns for Visualization](#step-4-normalize-data-columns-for-visualization)
   - [Step 5: Create Layout of the Dashboard](#step-5-create-layout-of-the-dashboard)
   - [Step 6: Add Interactivity with Callbacks](#step-6-add-interactivity-with-callbacks)
   - [Step 7: Run the Application](#step-7-run-the-application)
5. [Running the Dashboard](#running-the-dashboard)
6. [Conclusion](#conclusion)

## Introduction

This project focuses on creating an interactive dashboard for multimodal data, allowing the visualization of several types of charts and metrics. It includes a variety of visualization elements, such as:
- **Cluster Maps**: Display geographic clusters of persons and vehicles.
- **Heatmaps**: Show spatial data like "greeness" and "noise".
- **Histograms**: For detailed distributions of data features.
- **Correlation Analysis**: A correlation matrix to assess relationships among numerical features within specific places.

You will be able to manipulate the plots interactively by using the dropdown filters for metrics or specific data places.

## Install Required Libraries

Before starting, ensure that the required Python libraries are installed. Use the following command to install them:

```bash
pip install dash dash-bootstrap-components pandas plotly numpy pathlib

```

Dash: Main library to create the web dashboard.
dash_bootstrap_components: For easy styling with Bootstrap for better and responsive layout.
pandas: For loading and managing the dataset.
plotly: For plotting various charts and visualizations.
Project Structure
The project is composed of:

app.py: Python script containing the dashboard’s functionality and layout.
processed_mdf.csv: The dataset that stores the information you'll visualize.
The dataset should contain specific fields like greeness, noise, person, vehicles, and lat/lon, which are utilized for various charts and features.
## Create a Virtual Environment
Run the following command in your project's root directory:
Windows (Command Prompt)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## Understanding the Code


Step 1: Import Required Libraries
The first thing we need is to import the libraries necessary to build our dashboard and plot the data. Here are the main ones:

'''from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path


Dash: Used to create the web-based dashboard.
dash_bootstrap_components: For easy styling using Bootstrap framework.
pandas: Used to read, manipulate, and process the dataset.
plotly: Helps in creating various kinds of interactive plots.
numpy: Needed for data manipulation (though not directly used here).
pathlib: Helps in handling file paths.'''

Step 2: Initialize the Dash Application
We initialize the Dash app with the following code, which is responsible for setting up the backend for the dashboard:

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

The external_stylesheets argument allows us to use Bootstrap for responsive design and better layout.

Step 3: Load Your Processed Data
The next step is to load the processed data into the script. You can load your dataset (processed_mdf.csv) as follows:
```bash
data_path = Path(r'D:/AllProjects/multi-modller/team1')
mdf = pd.read_csv('processed_mdf.csv')
```
Here, the processed_mdf.csv is the dataset containing data for features like greeness, noise, and lat/lon coordinates. Make sure the file path corresponds correctly to your local setup.

## Step 4: Normalize Data Columns for Visualization
Before visualization, we normalize the columns greeness and noise to make sure the data is scaled between 0 and 1. This helps in making the visual representation clear:
```bash

mdf['normalized_greeness'] = mdf['greeness'] / mdf['greeness'].max()
mdf['normalized_noise'] = mdf['noise'] / mdf['noise'].max()
```
This ensures that the values of greeness and noise fall within the same range, improving the display when plotted.
## Step 5: Create Layout of the Dashboard
Now, we define the structure (layout) of the dashboard. Dash uses rows and columns to structure the components. Here, you will add visual elements like dropdowns and graphs:
```bash
app.layout = dbc.Container([
    dbc.Row([html.H1("Multimodal Data Dashboard", className="text-center mt-3 mb-5", style={'color': 'cyan'})]),
    dbc.Row([
        dbc.Col([html.H4("Person and Vehicle Clusters", className="mt-3", style={'color': 'orange'}), dcc.Graph(id='cluster-map')], md=6),
        dbc.Col([html.H4("Greeness & Noise Levels Heatmap", className="mt-3", style={'color': 'lightgreen'}), dcc.Graph(id='heatmap')], md=6),
    ])
])
```
The dashboard uses Grid Layout: Rows and Columns to create a responsive interface.
Graph Components: These will display interactive plots such as cluster maps and heatmaps.
Heading Styling: Each heading is styled with different colors using inline CSS.
## Step 6: Add Interactivity with Callbacks
Dash enables interactivity using Callbacks. For example, when a user interacts with a dropdown menu or changes a parameter, the graph updates accordingly. Below is an example for the heatmap graph:
```bash
@app.callback(Output('heatmap', 'figure'), Input('heatmap-metric', 'value'))
def update_heatmap(metric):
    heatmap_fig = go.Figure(go.Densitymapbox(lat=mdf['lat'], lon=mdf['lon'], z=mdf[metric], radius=20))
    return heatmap_fig
```
When the user selects a different metric (such as greeness or noise), this callback is triggered, and the heatmap is updated in real-time.

## Step 7: Run the Application
Finally, to make the dashboard viewable in a web browser, use the following code to run the application:
```bash
if __name__ == "__main__":
    app.run_server(debug=True)
```
This starts a local server at http://127.0.0.1:8050/ where the dashboard is displayed.
## Running the Dashboard
To run the dashboard, follow these steps:

Save the Python script as dashboard.py.
Ensure you have installed all the required libraries (dash, plotly, pandas, dash-bootstrap-components).
Place your processed_mdf.csv file in the correct location or adjust the file path in the script.
Run the Python script:
```bash
py dashboard.py
```
Your dashboard will be accessible locally at http://127.0.0.1:8050/.

## Conclusion
This project demonstrates how to build an interactive dashboard for visualizing multimodal data. Key skills learned include:

Working with Dash and Plotly for creating dynamic visualizations.
Handling various types of plots including cluster maps, heatmaps, histograms, and correlation analysis.
Using callbacks to add interactivity between user input and visual components.
This provides a solid foundation for anyone interested in creating interactive data visualization dashboards using Python. We hope this guide helps you in furthering your skills in data visualization and web development.

Good luck, and happy coding!
