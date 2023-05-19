import streamlit as st
import pickle
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import plotly.graph_objects as go

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    axis_format = dict(
        title_font_size=20,
        tickfont_size=16,
        showline=True,
        color="RGBA(1, 135, 73, 0.3)",
        tickcolor="RGBA(1, 135, 73, 0.3)",
        showgrid=True,
        griddash="dash",
        linewidth=1,
        gridcolor="RGBA(1, 135, 73, 0.3)"
    )
    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_x4j4bs6z.json"  background="transparent"  speed="1.9"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "Hydraulic structures",
                "Water cycle",
                "Drainage basin",
                "Hyetograph",
                "Runoff",
                # "Infiltration",
                # "Rainfall-runoff models",
                "Design storm",
                "IDF curve"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
        Pearson Education Inc., Boston.
        """
    
        cols = st.columns(2)
        with cols[0]:
            r"""
            [![Github Repo](https://img.shields.io/static/v1?label=&message=Repository&color=black&logo=github)](https://github.com/edsaac/NU.CIVENV340)
            """
        with cols[1]:
            r""" [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""
    
    ####################################################################
    
    if option == "Hydraulic structures":
        r"""
        ## Dams & spillways
        """ 
        "### Elements of a dam"
        url = "https://www.fema.gov/sites/default/files/2020-08/fema_911_pocket_safety_guide_dams_impoundments_2016.pdf"
        st.caption("Pocket Safety Guide for Dams and Impoundments (FEMA P-911)<br>" + f"Source: [{urlparse(url).hostname}]({url})", unsafe_allow_html=True)
        st.image("assets/img/embankment.png", use_column_width=True)

        
        r"""
        &nbsp;

        ### Dam classification

        """

        tabs = st.tabs([
            "**Gravity**",
            "**Arch**",
            "**Embankment**",
            "**Buttress**"
        ])

        imgs = [
            "https://upload.wikimedia.org/wikipedia/commons/9/94/Dworshak_Dam.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/1f/Presa_de_El_Atazar_-_01.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/1c/Tataragi_Dam10n4272.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/9d/Lake_Tahoe_Dam-10.jpg"
        ]

        captions =[
            "Dworshak Dam (ID, USA)",
            "Presa de El Atazar (Madrid, España)",
            "Kurokawa Dam - 多々良木ダム (Asago, Japan)",
            "Lake Tahow Dam (CA, USA)"
        ]

        for tab,img_url,caption in zip(tabs, imgs, captions):
            with tab:
                st.caption(rf"""
                    **{caption}** <br>
                    Source: [{urlparse(img_url).hostname}]({img_url})
                    """, unsafe_allow_html=True
                )

                st.image(img_url, use_column_width=True)

        r"""
        *******
        ## Stilling basin (outlet erosion control)
        """

        img_url = "https://media.defense.gov/2019/Oct/17/2002196661/780/780/0/190326-A-A1412-007.JPG"
        source = "https://www.spa.usace.army.mil/Media/News-Stories/Article/1991774/john-martin-dams-concrete-stilling-basin-in-excellent-condition-after-first-ins/"
        st.caption(rf"""
            **John Martin Dam's concrete stilling basin (Highland, UK)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

        url = "https://www.youtube.com/watch?v=TuQUf-nieVY"
        st.caption(f"**Spillways and outlet works** <br>\n Source: Association of State Dam Safety Officials (ASDSO) [youtube.com/@associationofstatedamsafet8080]({url})", unsafe_allow_html=True)
        st.video(url)

        r"""
        *******
        ## Culverts

        |Inlet| Outlet| Notes |
        |:----|:------|:------|
        |Submerged|Submerged|Pressurized pipe flow|
        |Submerged|Submerged|Full pipe flow with free-discharge outlet|
        |Submerged|Unsubmerged|Partial full pipe flow|
        |Unsubmerged|Unsubmerged|Open-channel flow|

        &nbsp;

        """
        img_url = "https://upload.wikimedia.org/wikipedia/commons/a/ad/Culvert_under_the_A835_-_geograph.org.uk_-_3466116.jpg"
        source = "https://www.geograph.org.uk/photo/3466116"
        st.caption(rf"""
            **Culvert under the A835 (Highland, UK)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)


    elif option == "Water cycle":
        r"""
        ## Water cycle
        """
        
        img_url = "assets/img/USGS_WaterCycle_English_ONLINE_20230302.png"
        source = "https://labs.waterdata.usgs.gov/visualizations/water-cycle/index.html#/"
        st.caption(rf"""
            **The Water Cycle** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

        "*****"
        img_url = "https://agupubs.onlinelibrary.wiley.com/cms/asset/1c96a142-6fc9-48ee-b1d1-6f5b41d77329/eft21123-fig-0001-m.jpg"
        source = "https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021EF002613"

        st.caption(rf"""
            **A conceptual model** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

    elif option == "Drainage basin":
        r"""
        ## Watersheds
        """

        img_url = "https://upload.wikimedia.org/wikipedia/commons/0/02/Amazonriverbasin_basemap.png"
        source = "https://commons.wikimedia.org/wiki/File:Amazonriverbasin_basemap.png"
        st.caption(rf"""
            **Amazon river basin** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

        with st.expander("Check **Hydrosheds**, global hydrography derived from spaceborne elevation data"):
            img_url = "https://uploads-ssl.webflow.com/602ebbdd5021f30e81efbad9/62536860d9d1c6fe627d42ce_HydroSHEDS_zoom-p-1080.jpeg"
            source = "https://www.hydrosheds.org/products/hydrosheds"
            st.caption(rf"""
                **Amazon river basin** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)
            
            "****"
            _, col, _ = st.columns([1,10,1])
            with col:
                url = "https://doi.org/10.1029/2008eo100001"
                st.markdown(
                    fr"""
                    Also check:

                    ⏺ Lehner, B., Verdin, K., & Jarvis, A. (2008). <br>
                    **New Global Hydrography Derived From Spaceborne Elevation Data**. <br>
                    *In Eos, Transactions American Geophysical Union (Vol. 89, Issue 10, p. 93)* <br>
                    DOI: [10.1029/2008eo100001]({url})
                    
                    """, unsafe_allow_html=True)


        img_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/WBD_SubRegions_24x18.png"
        source = "https://www.usgs.gov/media/images/watershed-boundary-dataset-subregions-map"
        
        st.caption(rf"""
            **Watershed Boundary Dataset Map** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

        r"""
        *******
        ## Sewage systems
        """
        img_url = "assets/img/sewer_system_map_Bogotá.png"
        source = "https://www.acueducto.com.co/wassigue6/MapasGeoportal"
        
        st.caption(rf"""
            **Map of sewer system in Bogotá (Colombia)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )

        st.image(img_url, use_column_width=True)

        "******"
        cols = st.columns(2)
        with cols[0]:
            img_url = "https://i0.wp.com/civilengineerspk.com/wp-content/uploads/2014/03/002.jpg"
            source = "https://www.civilengineerspk.com/design-of-sewer-system/"
        
            st.caption(rf"""
                **Combined v. separate sewer systems** <br>
                Dry weather <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)
        
        with cols[1]:
            img_url = "https://i0.wp.com/civilengineerspk.com/wp-content/uploads/2014/03/001.jpg"
            source = "https://www.civilengineerspk.com/design-of-sewer-system/"
        
            st.caption(rf"""
                **Combined v. separate sewer systems** <br>
                Wet weather <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)

    elif option == "Hyetograph":
        
        r"""
        ## Hyetograph ↦ plot of rainfall intensity over time
        """
        
        st.info(
            r"""
            Gather data from the USGS database on:
            - https://help.waterdata.usgs.gov/faq/automated-retrievals
            - https://waterdata.usgs.gov/nwis/current/?type=precip&group_key=state_cd
            """
        )

        rain = get_hydrologic_data("Precipitation")
        rain["per-hour"] = rain["value"].rolling(12, center=False).sum()
            
        figs = dict()

        figs["raw"] = go.Figure([
            go.Bar(
                x=rain["dateTime"],
                y=rain["value"]
            )
        ])

        figs["per-hour"] = go.Figure([
            go.Bar(
                x=rain["dateTime"],
                y=rain["per-hour"]
            )
        ])

        titles = [
            "Total rainfall in 5 min [in]",
            "Rainfall intensity [in/hr]"
        ]
        for t,fig in zip(titles,figs.values()):
            fig.update_layout(
                title_text = '''Data from a USGS rain gauge. <br>Source <a href="https://waterdata.usgs.gov/monitoring-location/414542087380901/#parameterCode=00045&period=P30D">Waterdata - USGS</a>''',
                height=500,
                yaxis=dict(
                    title=t,
                    **axis_format),
                xaxis=dict(
                    title="Datetime",
                    **axis_format),
                hovermode='closest',
                hoverlabel=dict(font_size=18),
            )

        tabs = st.tabs(["Raw data", "Aggregated per hour"])

        for tab,fig in zip(tabs, figs.values()):
            with tab:
                st.plotly_chart(fig, use_container_width=True)

        "*****"
        cols = st.columns([1,2])
        with cols[0]:
            "&nbsp;\n\n&nbsp;\n\n"
            st.info("What is an inch of rain?")

        with cols[1]:
            img_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/wss-rain-storm-colorado.jpg"
            source = "https://www.usgs.gov/media/images/rainstorms-can-be-localized-or-widespread"
            
            st.caption(rf"""
                **A localized heavy summer rainstorm in Colorado** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)

        r"""
        ******
        ### How is rainfall measured? &nbsp; ↝  &nbsp; The tipping bucket rain gauge
        """

        cols = st.columns(4)

        with cols[0]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/4/42/Exterior_tipping_bucket.JPG"
            source = "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Exterior_tipping_bucket.JPG"
            st.caption(rf"""
                **Exterior** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)
        
        with cols[1]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/9/90/Interior_tipping_bucket.JPG"
            source = "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Interior_tipping_bucket.JPG"
            st.caption(rf"""
                **Interior** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)

        with cols[2]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/6/67/Tipping_Bucket_Recorder.JPG"
            source = "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Tipping_Bucket_Recorder.JPG"
            st.caption(rf"""
                **Recording** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)

        with cols[3]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/f/fd/Close_up_chart.JPG"
            source = "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Close_up_chart.JPG"
            st.caption(rf"""
                **Close-up** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)

        "******"
        
        cols = st.columns([1,3])
        with cols[0]:
            "&nbsp;"
            "&nbsp;"

            year = st.select_slider("Year", range(2000,2023,1), 2022)
            month = st.select_slider("Month", range(1,13,1), 12)
            which = st.selectbox("Map", ["Monthly total", "Deviation from average"])
        with cols[1]:
            source = "https://www.climate.gov/maps-data/data-snapshots/snapshot?id=8701"
            
            if which == "Monthly total":
                img_url = f"https://www.climate.gov/data/Precipitation--Monthly--Total--CONUS/02-large/Precipitation--Monthly--Total--CONUS--{year}-{month:02d}-00--large.png"
            
                st.caption(rf"""
                    **Monthly total precipitation** <br>
                    Source: [{urlparse(source).hostname}]({source})
                    """, unsafe_allow_html=True
                )
            elif which == "Deviation from average":
                img_url = f"https://www.climate.gov/data/Precipitation--Monthly--Difference-from-average--CONUS/02-large/Precipitation--Monthly--Difference-from-average--CONUS--{year}-{month:02d}-00--large.png"
                
                st.caption(rf"""
                    **Monthly difference from average** <br>
                    Source: [{urlparse(source).hostname}]({source})
                    """, unsafe_allow_html=True
                )
            
            st.image(img_url, use_column_width=True)


    elif option == "Runoff":
        r"""
        ## Hydrograph ↦ plot of discharge over time
        """
        
        flow = get_hydrologic_data("Streamflow")
            
        fig = go.Figure([
            go.Scatter(
                x=flow["dateTime"],
                y=flow["value"]
            )
        ])

        fig.update_layout(
            title_text = '''Data from a USGS station. <br>Source <a href="https://waterdata.usgs.gov/monitoring-location/02223500/#parameterCode=00065&period=P30D">Waterdata - USGS</a>''',
            height=500,
            yaxis=dict(
                title="Streamflow [ft³/s]",
                **axis_format),
            xaxis=dict(
                title="Datetime",
                **axis_format),
            hovermode='closest',
            hoverlabel=dict(font_size=18),
        )

        st.plotly_chart(fig, use_container_width=True)

        "*****"
        cols = st.columns(2)
        with cols[0]:
            r"""
            &nbsp;

            &nbsp;
            """
            st.info("How are rain and runoff related?")

        with cols[1]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/9/95/Runoff_of_soil_%26_fertilizer.jpg"
            source = "https://commons.wikimedia.org/wiki/File:Runoff_of_soil_&_fertilizer.jpg"
            
            st.caption(rf"""
                **Runoff from a farm field in Iowa** <br>
                Source: [{urlparse(source).hostname}]({source})
                """, unsafe_allow_html=True
            )
            st.image(img_url, use_column_width=True)
    
    elif option == "Design storm":
        r"""
        ## Design storms

        |Parameter|Description|Units|
        |--------:|:----|:----:|
        |**Return period**| Average time between occurences of a hydrological event | Years |
        |**Rainfall intensity**| Rate of precipitation | Length/Time |
        |**Total rainfall**| Depth of precipitation over the time of the event | Length |
        |**Average intensity**| Total rainfall divided by the storm duration | Length |
        |**Spatial distribution**| Total rainfall divided by the storm duration | - |

        &nbsp;
        """

        url = "https://jeffskwang.github.io/"
        st.button('Go to rain/runoff example', on_click=open_page, args=(url,), use_container_width=True)

    elif option == "IDF curve":
        r"""
        ## IDF: Intensity-Duration-Frequency curves

        $$
            \textsf{Empirical:} \quad I(t) = \dfrac{a}{\left( t + c \right)^n}
        $$
        """

        cols = st.columns([3,1])
        with cols[0]:
            st.image("assets/img/IDF curve Ohare IL.png", use_column_width=True)
        with cols[1]:
            source = "https://hdsc.nws.noaa.gov/hdsc/pfds/pfds_map_cont.html"
            st.caption(rf"""
                &nbsp;

                &nbsp;

                Source: NOAA's National Weather Service <br>
                [Precipitation Frequency Data Server (PFDS)]({source})""",
                unsafe_allow_html=True
            )
            st.image("https://hdsc.nws.noaa.gov/hdsc/pfds/imgs/yrs_legend_pds.png")

        # cols = st.columns([2,2])
        # with cols[0]:
        #     st.map({"LAT":[42.0660], "LON":[-87.7332]}, zoom=4, use_container_width=True)
        # with cols[1]:
        #     st.image("https://hdsc.nws.noaa.gov/hdsc/pfds/plots/42.0660_-87.7332_ams_IDF_in_ari.png", use_column_width=True)

        url = "https://hdsc.nws.noaa.gov/hdsc/pfds/pfds_map_cont.html"
        st.button('Go to NOAA Precipitation Frequency Data Server', on_click=open_page, args=(url,), use_container_width=True)
        

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"


def open_page(url):
    open_script= f"""
        <script type="text/javascript">
            window.open('{url}', '_blank').focus();
        </script>
    """
    st.components.v1.html(open_script)

@st.cache_data
def get_hydrologic_data(variable):
    
    if variable == "Precipitation": key = 0
    elif variable ==  "Streamflow":  key = 1
    elif variable ==  "Stage":  key = 2
    else: st.error("No variable was specified")
    
    url = "https://waterservices.usgs.gov/nwis/iv/?sites=02223500&startDT=2023-03-13T18:16:05.289-04:00&endDT=2023-04-12T18:16:05.289-04:00&siteStatus=all&format=json"
    r = requests.get(url, stream=True)
    data = r.json()
    df = pd.DataFrame(data["value"]["timeSeries"][key]["values"][-1]["value"])
    # st.json(data)
    # st.dataframe(df)
    df["dateTime"] = pd.to_datetime(df["dateTime"], format=r"%Y-%m-%d %H:%M:%S", utc=True)
    df["value"] = pd.to_numeric(df["value"])
    
    return df
    

# @st.cache_data
# def get_rain_data():
    
#     from datetime import datetime, timezone

#     url = "https://waterservices.usgs.gov/nwis/iv/?sites=414542087380901&period=P30D&format=json"
#     r = requests.get(url, stream=True)
#     data = r.json()
    
#     # Only extract the values for precipitation
#     rain = pd.DataFrame(data["value"]["timeSeries"][1]["values"][0]["value"])
#     rain["dateTime"] = pd.to_datetime(rain["dateTime"], format=r"%Y-%m-%d %H:%M:%S", utc=True)
#     rain["value"] = pd.to_numeric(rain["value"])

#     print(rain.dtypes)
#     start_date = datetime(2023,3,22,18,00,00, tzinfo=timezone.utc)
#     end_date   = datetime(2023,3,23,18,00,00, tzinfo=timezone.utc)

#     return rain[np.logical_and(rain["dateTime"] > start_date, rain["dateTime"] < end_date)]

if __name__ == "__main__":
    main()

# elif option == "Infiltration":
#     r"""
#     ## Infiltration and groundwater recharge
#     """
    
#     cols = st.columns(2)

#     with cols[0]:
#         r"""
#         Something
#         """

#     with cols[1]:
#         img_url = "https://placekitten.com/400/400"
#         source = "https://placekitten.com/400/400"
        
#         st.caption(rf"""
#             **Infiltration cat** <br>
#             Source: [{urlparse(source).hostname}]({source})
#             """, unsafe_allow_html=True
#         )
#         st.image(img_url, use_column_width=True)

# elif option == "Rainfall-runoff models":
#     r"""
#     ## Rainfall-runoff models
#     """

#     cols = st.columns(2)

#     with cols[0]:
#         r"""
#         Mass balance between evapotranspiration, rainfall, runoff and infiltration
#         """

#     with cols[1]:
#         img_url = "https://upload.wikimedia.org/wikipedia/commons/8/80/Surface_water_cycle.svg"
#         source = "https://en.wikipedia.org/wiki/Runoff_model_(reservoir)#/media/File:Surface_water_cycle.svg"
        
#         st.caption(rf"""
#             **Runoff from the water balance** <br>
#             Source: [{urlparse(source).hostname}]({source})
#             """, unsafe_allow_html=True
#         )
#         st.image(img_url, use_column_width=True)