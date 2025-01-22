# Multimedia Data Analysis and Visualization Pipeline

This project performs comprehensive data processing, visualization, and analysis of multimedia data, including images, audio, and geospatial data. The pipeline encompasses clustering, correlation analysis, and creating interactive visualizations to explore spatial and temporal relationships in the data.

---

## Project Overview

### 1. Data Loading and Preprocessing
- Data from CSV files is loaded into Pandas DataFrames.
- Key columns like `mediaID` and `observationID` are converted to appropriate data types for efficient processing.

### 2. Image Data Processing
- Image paths are extracted, and additional attributes are calculated, including:
  - **Brightness**: Using a custom `calculate_brightness` function to compute RGB brightness averages.
  - **Greenness**: Vegetation detection using the `calculate_greeness` function based on RGB channel differences.

### 3. Audio Data Processing
- Audio files are analyzed for noise levels using `librosa`.
- The `calculate_noise_level` function computes Root Mean Square (RMS) noise levels in decibels (dB).

### 4. Clustering and Geospatial Visualization
- Image entries are merged with metadata for clustering.
- Latitude and longitude data are clustered using K-Means to group spatial locations.
- Interactive visualizations, such as scatter maps and heatmaps, are created with Plotly.

### 5. Correlation Analysis
- Relationships among numerical features like `brightness`, `greenness`, and `noise` are visualized using heatmaps.
- Correlations are analyzed for:
  - Spatial clusters
  - Specific times of day (hourly)

---
---

## Outputs

The script generates various types of outputs to aid in analysis and visualization:

### 1. Geospatial Visualization
- **Interactive Map**: Clusters based on geospatial attributes (`latitude`, `longitude`) are plotted on an OpenStreetMap. Interactive markers display brightness, greenness, and noise levels when hovered over.

### 2. Histograms
- **Feature Distributions**:
  - `Brightness`: Distribution of brightness levels in processed images.
  - `Greenness`: Greenness index distribution to evaluate vegetation presence.
  - `Noise`: Noise levels (in dB) computed from audio files.
  - `Persons`/`Vehicles`: Counts of persons and vehicles detected from metadata.

### 3. Heatmaps
- **Correlation Matrices**:
  - Show relationships between attributes like `brightness`, `greenness`, `noise`, and detected entities.
  - Analysis is performed for specific geospatial clusters and time intervals.

### 4. Temporal Analysis
- **Hour-by-Hour Trends**:
  - Visualizes hourly variations for attributes (`brightness`, `greenness`, etc.).
  - Enables understanding of temporal effects on spatial features.

### 5. Summary Reports
- Textual summaries and statistical data are exported to support decision-making. These include:
  - Cluster sizes and centroids.
  - Key attribute summaries per cluster.

---

## Contribution

We welcome all contributors to enhance this project!  
To contribute:  
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed information about the feature or fix.

---

## Author

Developed by **[Ghulam Rabbani]** as part of multimedia data analytics research and development.

---

## License

This project is distributed under the **MIT License**. See the LICENSE file for details.


## Prerequisites

Install the required Python libraries:
```bash
pip install pandas numpy librosa opencv-python matplotlib seaborn plotly tqdm sklearn
pip install ffmpeg-python nbformat --upgrade
