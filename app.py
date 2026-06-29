import streamlit as st
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch

st.set_page_config(
    page_title="Stellenbosch Vegetation Change Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)
change_cmap = LinearSegmentedColormap.from_list(
    "change",
    ["red", "white", "green"]
)

# st.markdown("""
# <style>
# .stApp {
#     background-color: #f5f7fa;
# }
# </style>
# """, unsafe_allow_html=True)

def calculate_ndvi(red_path, nir_path):
    red = rasterio.open(red_path).read(1).astype(float) #read red band
    nir = rasterio.open(nir_path).read(1).astype(float) #read nir band
    return (nir - red) / (nir + red + 1e-10)


st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 8rem;
    padding-right: 8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; font-size:60px;'>
Stellenbosch Vegetation Change Detector
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: gray;'>
Developed by Olivia Connellan | Stellenbosch University
</p>
""", unsafe_allow_html=True)

# st.markdown("""
# <p style='text-align: center; font-size:18px;'>
# Compare Sentinel-2 NDVI images between two years.
# </p>
# """, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 24px;
}
</style>
""", unsafe_allow_html=True)

ndvi_table = pd.DataFrame({
    "NDVI Value": [
        "< 0",
        "0.0 – 0.2",
        "0.2 – 0.5",
        "0.5 – 0.8"
    ],
    "Meaning": [
        "Water, clouds, shadows",
        "Bare soil, urban areas",
        "Grassland and sparse vegetation",
        "Dense, healthy vegetation"
    ]
})

with st.sidebar:
    with st.expander("ℹ️ About this Application"):
            st.write("""
            The Stellenbosch Vegetation Change Detector compares Sentinel-2 satellite imagery 
            from two different years using the Normalized Difference Vegetation Index (NDVI). It 
            identifies areas where vegetation has increased, decreased, or remained relatively 
            stable over time.
            """)
    with st.expander("🌿 What is NDVI?"):
            st.write("""
            NDVI (Normalized Difference Vegetation Index) is a widely used remote sensing index
            that measures vegetation health using the red and near-infrared bands of satellite 
            imagery.
            """)
            st.table(ndvi_table)
    with st.expander("📈 How does the comparison work?"):
            st.write("""
            The application:
                     
                1. Loads Sentinel-2 imagery from two selected years.
                2. Calculates NDVI for each year.
                3. Computes the difference:
                    NDVI₂ − NDVI₁
                4. Classifies pixels as vegetation gain, vegetation loss, or no significant change 
                    based on the selected threshold.
            """)
    with st.expander("🎨 Understanding the Maps"):
        st.write("""
        ## NDVI Maps
            🟢 Green
                - Healthy vegetation
            🟡 Yellow
                - Sparse vegetation
            🔴 Red     
                - Bare soil, urban areas or low vegetation
        ## Change Map
            🟢 Green
                - Vegetation increased
            ⚪ White
                - Little or no change
            🔴 Red
                - Vegetation decreased
        """)
    with st.expander("📊 Understanding the Statistics"):
        st.markdown("""
        <h4 style="margin-bottom:0px;">Vegetation Loss</h4>

        <p style="margin-top:0;">
        Percentage of pixels whose NDVI decreased by more than the selected threshold.
        </p>

        <h4 style="margin-bottom:0px;">Vegetation Gain</h4>

        <p style="margin-top:0;">
        Percentage of pixels whose NDVI increased by more than the selected threshold.
        </p>

        <h4 style="margin-bottom:0px;">Net Vegetation Change</h4>

        <p style="margin-top:0;">
        Calculated as <strong>Vegetation Gain − Vegetation Loss</strong>. A positive value indicates an overall increase in vegetation, while a negative value indicates an overall decrease.
        </p>
        """, unsafe_allow_html=True)
    with st.expander("🎚 Threshold"):
        st.markdown("""
        The threshold controls how much NDVI must change before a pixel is classified as 
        vegetation gain or vegetation loss.

        **Small Threshold**
        - Detects subtle changes
        - More sensitive
                    
        **Large Threshold**
        - Detects only major changes
        - Reduces noise
        
        """, unsafe_allow_html=True)
    with st.expander("📡 Data Source"):
        st.markdown("""
        **Satellite:** Sentinel-2A and Sentinel-2B (Copernicus Programme)
        
        **Data Provider:** Copernicus Data Space Ecosystem
        
        **Imagery Access:** Copernicus Browser
        
        **Spatial Resolution:** 10 m
                
        **Bands Used:**
        - Band 4 – Red (665 nm)
        - Band 8 – Near Infrared (842 nm)
        
        """, unsafe_allow_html=True)



st.write("")

cc1, cc2 = st.columns(2)
with cc1:
    left, centre, right = st.columns([1, 10, 1])
    with centre:
        with st.container(border=True, height=300):
            st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="font-size:26px; font-weight:bold;">Analysis Settings</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.write("")

            col1, col2, col3, col4= st.columns([1,8,8,1])


            with col2:
                year1 = st.selectbox("Select first year",
                                ["2015","2016","2017" , "2018", "2019" ,"2020", "2021", "2022", "2023", "2024", "2025"], index=0)

            with col3:
                year2 = st.selectbox("Select second year", 
                                ["2015","2016","2017" , "2018", "2019" ,"2020", "2021", "2022", "2023", "2024", "2025"], index=1)

            st.write("")
            c1,c2,c3,c4,c5 = st.columns([1,6,1,4,1])
            with c2:
                threshold = st.slider("Change threshold", 0.05, 0.4, 0.2)

            # colum1, colum2, colum3 = st.columns([5,5,4])
            with c4:
                st.write("")
                generate = st.button("Generate Change Map",
                                    help="Calculates NDVI for both years and displays the vegetation change results.")
with cc2:
    left, centre, right = st.columns([1, 10, 1])
    with centre:
        with st.container(border=True, height=300):
                #st.subheader("Vegetation Change Results")
            st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-size:26px; font-weight:bold;">Vegetation Change Results</div>
                </div>
                """, unsafe_allow_html=True)
            

            if not generate:
                st.info("Click Generate Change Map to view results.")

            else:
                ndvi_1 = calculate_ndvi(f"data/{year1}/B04.tiff", f"data/{year1}/B08.tiff")
                ndvi_2 = calculate_ndvi(f"data/{year2}/B04.tiff", f"data/{year2}/B08.tiff")

                change = ndvi_2 - ndvi_1

                classified = np.zeros(change.shape)
                # 1 = loss
                classified[change < -threshold] = 1
                # 2 = gain
                classified[change > threshold] = 2

                loss_pixels = np.sum(change < -threshold) # all pixels < -0.2 significant vegetation losses  
                gain_pixels = np.sum(change > threshold)  # vegetation gains
                total_pixels = change.size # total number of pixels

                loss_percent = 100 * loss_pixels / total_pixels
                gain_percent = 100 * gain_pixels / total_pixels

                st.write("")

                net_change = gain_percent - loss_percent
                net_colour = "#2ca02c" if net_change >= 0 else "#d62728"
                net_bg = "#ecf8ec" if net_change >= 0 else "#fdecec"
                net_icon = "🌱" if net_change >= 0 else "⚠️"

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="font-size:18px;">Vegetation loss</div>
                        <div style="font-size:24px; font-weight:bold;">{loss_percent:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="font-size:18px;">Vegetation gain</div>
                        <div style="font-size:24px; font-weight:bold;">{gain_percent:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="font-size:18px;">Net change</div>
                        <div style="font-size:24px; font-weight:bold;">{net_change:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.write("")

                
                coll1, coll2, coll3 = st.columns([2,5,3])
                with coll2:
                    st.markdown(
                        f"""
                        <div style="
                            text-align:center;
                            background-color:{net_bg};
                            padding:6px;
                            border-radius:12px;
                            border:1px solid {net_colour};
                            color:{net_colour};
                            font-size:19px;
                            font-weight:bold;
                            width: 250px;
                        ">
                            {net_icon} Net vegetation change: {net_change:.2f}%
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
            st.write("")

if generate:
    st.write("")
    cl1,cl2,cl3 = st.columns([1,70,1])
    with cl2:
        with st.container(border=True):
            c1,c2,c3 = st.columns(3)
            with c2:
                st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="font-size:26px; font-weight:bold;">NDVI Comparison Maps</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.write("")
            st.markdown("<br>", unsafe_allow_html=True)
            fig, axes = plt.subplots(1, 3, figsize=(14, 12))
            axes = axes.flatten()

            axes[0].imshow(ndvi_1, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
            # Low NDVI → Red     Medium  → Yellow     High NDVI → Green  
            axes[0].set_title(f"NDVI {year1}")

            axes[1].imshow(ndvi_2, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
            axes[1].set_title(f"NDVI {year2}")

            im = axes[2].imshow(change, cmap=change_cmap, vmin=-0.5, vmax=0.5)
            axes[2].set_title(f"NDVI Change {year1} → {year2}")

            for ax in axes:
                ax.axis("off")

            fig.subplots_adjust(right=0.88)
            fig.colorbar(im, ax=axes, fraction=0.011, pad=0.02, label="NDVI Change")

            axes[2].axis("off")
            # fig.tight_layout(pad=0.5)
            st.pyplot(fig)  #displays final figure

