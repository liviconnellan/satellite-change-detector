import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt


#takes in a red file and a nir file and outputs an NDVI image
def calculate_ndvi(red_path, nir_path):
    red = rasterio.open(red_path).read(1).astype(float) #read red band
    nir = rasterio.open(nir_path).read(1).astype(float) #read nir band
    return (nir - red) / (nir + red + 1e-10)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# creates heading
st.markdown("""
<h1 style='text-align: center;'>
Stellenbosch Vegetation Change Detector
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: gray;'>
Developed by Olivia Connellan | Stellenbosch University
</p>
""", unsafe_allow_html=True)

# adds normal text under
st.markdown("""
<p style='text-align: center; font-size:18px;'>
Compare Sentinel-2 NDVI images between two years.
</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Information")

    with st.expander("About this project"):
        st.write("""
        This application uses Sentinel-2 satellite imagery to detect
        vegetation changes around Stellenbosch using NDVI
        (Normalized Difference Vegetation Index).
        """)
    with st.expander("How to use"):
        st.write("""
            1. Select two years
            2. Adjust the change threshold
            3. Click 'Generate Change Map'
            4. Review vegetation gain/loss statistics
            """)


# creates drop down
year1 = st.selectbox("Select first year",
                      ["2015","2016","2017" , "2018", "2019" ,"2020", "2021", "2022", "2023", "2024", "2025"])
year2 = st.selectbox("Select second year", 
                     ["2015","2016","2017" , "2018", "2019" ,"2020", "2021", "2022", "2023", "2024", "2025"])

# creates slider
threshold = st.slider("Change threshold", 0.05, 0.4, 0.2)

# creates button (bellow code only run if clicked)
if st.button("Generate Change Map"):
    ndvi_1 = calculate_ndvi(f"data/{year1}/B04.tiff", f"data/{year1}/B08.tiff")
    ndvi_2 = calculate_ndvi(f"data/{year2}/B04.tiff", f"data/{year2}/B08.tiff")

    change = ndvi_2 - ndvi_1

    # counts changes
    loss_pixels = np.sum(change < -threshold) # all pixels < -0.2 significant vegetation losses  
    gain_pixels = np.sum(change > threshold)  # vegetation gains
    total_pixels = change.size # total number of pixels

    loss_percent = 100 * loss_pixels / total_pixels
    gain_percent = 100 * gain_pixels / total_pixels

    # display results
    st.subheader("Results")
    st.write(f"Vegetation loss: **{loss_percent:.2f}%**")
    st.write(f"Vegetation gain: **{gain_percent:.2f}%**")

    # creates 3 plots side by side
    #(1,3) --> 1 row, 3 columns
    # figsize=(18,6) --> width = 18, height = 6  (bigger nums = bigger numage)
    fig, axes = plt.subplots(1, 3, figsize=(24, 12))
    #fig = whole figure
    #axes contains 3 plots

    #first plot             colour ramp     min       max values
    # anything smaller than vmin --> dark red
    # anything larger than vmax --> dark green
    axes[0].imshow(ndvi_1, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
    # Low NDVI → Red     Medium  → Yellow     High NDVI → Green  
    axes[0].set_title(f"NDVI {year1}")

    axes[1].imshow(ndvi_2, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
    axes[1].set_title(f"NDVI {year2}")


    # plotting change
    # Red blue colour ramp
    # Negative values → Red     Zero  → White   Positive values → Blue
    # Red  = vegetation loss     Blue = vegetation gain
    im = axes[2].imshow(change, cmap="RdBu_r", vmin=-0.5, vmax=0.5)
    #im stores colour bar
    # fig.colorbar(im)  needs to know which image the colour bar belongs to
    axes[2].set_title(f"NDVI Change {year1} → {year2}")

    # remove axes
    for ax in axes:
        ax.axis("off")


   
    # creates colour bar
    # im uses change map
    # ax=axes   Reserve space beside ALL THREE plots and place one colour bar there
    fig.colorbar(im, ax=axes, shrink=0.7, label="NDVI Change")
    st.pyplot(fig)  #displays final figure

