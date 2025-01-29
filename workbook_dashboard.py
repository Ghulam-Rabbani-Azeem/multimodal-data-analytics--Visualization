from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path  # Helps with handling file paths

# Step 1: Initialize the Dash application
# Create an instance of the Dash application, linking it to a pre-made CSS stylesheet (from Bootstrap) for styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 2: Load Your Processed DataFrame
# Use pandas to read a CSV file containing the processed data. The data is stored in the `processed_mdf.csv` file.
# This dataset is then stored in the variable `mdf` for later use.
data_path = Path(r'D:\AllProjects\multi-modller\team1')  # Specifies the directory of the dataset
mdf = pd.read_csv('processed_mdf.csv')  # Load the data into a pandas dataframe

# Step 3: Normalize Columns for Visualization
# For better visualization, some numerical columns are normalized to have values in a common range (0 to 1). 
# Here, 'greeness' and 'noise' are normalized by dividing by their maximum values.
# This ensures that we can easily compare and visualize the two metrics effectively.
mdf['normalized_greeness'] = mdf['greeness'] / mdf['greeness'].max()  # Normalize the 'greeness' column
mdf['normalized_noise'] = mdf['noise'] / mdf['noise'].max()  # Normalize the 'noise' column

# Step 4: Create Layout of the Dashboard
# The layout defines how the page looks. We will use components like rows and columns to divide content neatly.
app.layout = dbc.Container(
    [
        # This row includes the header with a title that spans the width of the container.
        dbc.Row([html.H1("Multimodal Data Dashboard", className="text-center mt-3 mb-5")]),
        
        # Define the first row of visualizations (Cluster Map and Heatmap)
        dbc.Row(
            [
                # Cluster Map Section - This will display person and vehicle clusters on a map.
                dbc.Col(
                    [
                        html.H4("Person and Vehicle Clusters", className="mt-3"),
                        # Placeholder for the cluster map visualization
                        dcc.Graph(id='cluster-map'),  
                    ],
                    md=6  # The column will take up half the width of the container (bootstrap grid)
                ),
                
                # Heatmap Section - This section shows greeness and noise levels on a map using a heatmap
                dbc.Col(
                    [
                        html.H4("Greeness & Noise Levels Heatmap", className="mt-3"),
                        # Placeholder for the heatmap
                        dcc.Graph(id='heatmap'),
                        # Label for dropdown to choose which metric (greeness or noise) to visualize
                        dbc.Label("Select Heatmap Metric:"),
                        dcc.Dropdown(
                            id="heatmap-metric",
                            options=[  
                                {'label': 'Greeness', 'value': 'normalized_greeness'},
                                {'label': 'Noise', 'value': 'normalized_noise'}
                            ],
                            value='normalized_greeness',  # Default value is greeness
                            clearable=False,  # Do not allow clearing the dropdown selection
                        ),
                    ],
                    md=6  # Column will take up the remaining width of the container
                ),
            ]
        ),
        
        # Define another row that includes a histogram and correlation analysis
        dbc.Row(
            [
                # Histogram Section - Allows selection of a numerical feature to display a histogram
                dbc.Col(
                    [
                        html.H4("Histogram Analysis", className="mt-5"),
                        dbc.Label("Select a Numerical Feature:"),
                        # Dropdown that allows selection of one of several numerical features for the histogram
                        dcc.Dropdown(
                            id='histogram-feature',
                            options=[{'label': col, 'value': col} for col in [
                                'person', 'vehicles', 'brightness', 'greeness', 'noise'
                            ]],
                            value='brightness',  # Default histogram feature
                            clearable=False,
                        ),
                        # This will display the generated histogram
                        dcc.Graph(id='histogram'),
                    ],
                    md=6  # Half width of the container for the histogram section
                ),
                
                # Correlation Section - Allows selection of a place to show a correlation matrix for the selected place
                dbc.Col(
                    [
                        html.H4("Correlation Analysis", className="mt-5"),
                        dbc.Label("Select a Place:"),
                        # Dropdown allowing the user to select a place (location) for correlation analysis
                        dcc.Dropdown(
                            id='place-dropdown',
                            options=[  
                                {'label': place, 'value': place} 
                                for place in sorted(mdf['place_name'].unique())  # List all unique places
                            ],
                            value=sorted(mdf['place_name'].unique())[0],  # Default place
                            placeholder="Select a place",
                            clearable=False,  # Default value will be preselected, no clearing
                        ),
                        # Placeholder for correlation heatmap display
                        dcc.Graph(id='correlation-heatmap'),
                    ],
                    md=6  # The correlation section will occupy half the width of the container
                ),
            ]
        ),
    ],
    fluid=True,  # Makes the layout fluid, which makes it responsive
    style={'backgroundColor': '#ADD8E6'}  # Apply a light blue background color for the entire page
)

# Step 5: Define Callbacks for Interactivity
# Callbacks allow the components to update dynamically based on user input (e.g., dropdown selections).
# The purpose of each callback is explained in detail.

# Callback for updating the Cluster Map based on the heatmap metric (either greeness or noise)
@app.callback(
    Output('cluster-map', 'figure'),
    Input('heatmap-metric', 'value')  # Input comes from the heatmap metric dropdown
)
def update_cluster_map(metric):
    # Initializing an empty list to collect traces (data points) for the map
    traces = []
    # Scale the marker size based on the maximum value of the 'person' column
    scaling_factor = 1000 / mdf['person'].max()

    # Loop through each cluster and add a new map layer to the traces list
    for cluster in sorted(mdf['place_cluster'].unique()):
        cluster_data = mdf[mdf['place_cluster'] == cluster]
        traces.append(
            go.Scattermapbox(
                lat=cluster_data['lat'],  # Latitude of each cluster's location
                lon=cluster_data['lon'],  # Longitude of each cluster's location
                mode='markers',  # Markers for the cluster's points
                marker=go.scattermapbox.Marker(
                    size=cluster_data['person'] * scaling_factor,  # Size of the markers scaled by the number of people
                    sizemode='area',
                    sizeref=2. * scaling_factor / (40. ** 2),  # Reference size for markers
                ),
                name=f"Place {cluster}",  # Name of the cluster as shown in the map legend
            )
        )

    # Create a map figure using the defined traces
    map_fig = go.Figure(traces)
    map_fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Style of the map, OpenStreetMap
            center=dict(lat=mdf['lat'].mean(), lon=mdf['lon'].mean()),  # Center the map on the average lat/lon
            zoom=12  # Set the zoom level
        ),
        height=400,  # Set the figure height for uniform size
        margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remove margins around the map
    )
    return map_fig

# Callback for updating the Heatmap based on the selected metric (greeness or noise)
@app.callback(
    Output('heatmap', 'figure'),
    Input('heatmap-metric', 'value')  # Input comes from the heatmap metric dropdown
)
def update_heatmap(metric):
    # Create a heatmap figure using a density map (color-based map showing intensity of values)
    heatmap_fig = go.Figure(
        go.Densitymapbox(
            lat=mdf['lat'],  # Latitude data for plotting
            lon=mdf['lon'],  # Longitude data for plotting
            z=mdf[metric],  # Choose the value of 'greeness' or 'noise' as the density value
            radius=20,  # Set the radius of each point on the heatmap
            colorscale="Viridis",  # Choose the color scale for heatmap visualization
            showscale=True,  # Show the color scale bar
        )
    )
    # Update layout to specify a consistent size for the heatmap
    heatmap_fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Style of the map
            center=dict(lat=mdf['lat'].mean(), lon=mdf['lon'].mean()),  # Center the map
            zoom=12  # Set zoom level for the map
        ),
        height=400,  # Consistent height across all images
        margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remove margins around the map
    )
    return heatmap_fig

# Callback for updating the Histogram based on the selected feature
@app.callback(
    Output('histogram', 'figure'),
    Input('histogram-feature', 'value')  # Input comes from the dropdown of feature selection for histogram
)
def update_histogram(feature):
    # Generate the histogram of the selected feature using Plotly Express
    hist_fig = px.histogram(mdf, x=feature, nbins=20, title=f"Distribution of {feature}")
    # Set height to ensure uniform size of the histogram
    hist_fig.update_layout(height=400)
    return hist_fig

# Callback for updating the Correlation Heatmap based on the selected place
@app.callback(
    Output('correlation-heatmap', 'figure'),
    Input('place-dropdown', 'value')  # Input comes from the place selection dropdown
)
def update_corr_heatmap(place_name):
    # If no data or an invalid place is selected, return a blank figure with a message
    if not place_name or mdf.empty:
        return go.Figure().update_layout(
            title="No data available for the selected place",
            margin=dict(l=40, r=40, t=40, b=40),
            height=400,  # Consistent height across graphs
        )
    
    # Filter the data for the selected place and calculate the correlation matrix of numeric columns
    place_data = mdf[mdf['place_name'] == place_name]
    numeric_columns = place_data.select_dtypes(include=['float64', 'int64']).columns
    
    # If there are no numeric columns, show a message indicating no data for correlation
    if numeric_columns.empty:
        return go.Figure().update_layout(
            title="No numeric data available for correlation",
            margin=dict(l=40, r=40, t=40, b=40),
            height=400,  # Consistent size
        )
    
    # Compute the correlation matrix and round to 3 decimal places
    corr_matrix = place_data[numeric_columns].corr().round(3)
    
    # Generate a correlation heatmap figure using Plotly Express
    fig = px.imshow(
        corr_matrix,
        text_auto=True,  # Display the correlation values in each cell of the heatmap
        color_continuous_scale='Viridis',  # Color scale
        title=f"Correlation Heatmap for {place_name}"
    )
    # Set layout details such as titles and margins for the correlation heatmap
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title="Features",
        yaxis_title="Features",
        height=400,  # Ensure consistency across figures
    )
    return fig

# Step 6: Run the Dash app
# If the script is executed directly, start the Dash application with debug mode enabled
if __name__ == "__main__":
    app.run_server(debug=True)
