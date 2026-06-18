# satellite-change-detector
Olivia Connellan

## Description
A Python-based Earth Observation tool that uses Sentinel-2 satellite imagery to detect vegetation changes over time.
The application calculates NDVI (Normalized Difference Vegetation Index), 
compares imagery from different years, and visualises vegetation gain and loss through an interactive Streamlit dashboard.

## Features
• Compare Sentinel-2 imagery from different years
• Calculate NDVI from Red and Near-Infrared bands
• Visualise vegetation change maps
• Calculate vegetation gain and loss statistics
• Interactive Streamlit interface

## How to Run
### Clone the repository
git clone <repository-url>

### Navigate to the project directory
cd satellite-change-detector

### Install dependencies
pip install -r requirements.txt

### Launch the application
streamlit run app.py

## Technology used
Python
Streamlit
Rasterio
NumPy
Matplotlib
Sentinel-2 Satellite Imagery
