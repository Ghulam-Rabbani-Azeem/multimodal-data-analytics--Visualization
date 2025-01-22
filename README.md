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

## Prerequisites

Install the required Python libraries:
```bash
pip install pandas numpy librosa opencv-python matplotlib seaborn plotly tqdm sklearn
pip install ffmpeg-python nbformat --upgrade
