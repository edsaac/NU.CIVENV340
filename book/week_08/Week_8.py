from typing import Literal
from urllib.parse import urlparse

import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from matplotlib.ticker import MultipleLocator
from dataretrieval.nwis import get_dv

from .subpages import oroville_dam, watershed_delimitation
from ..common import axis_format

TOC = Literal[
    "Water cycle",
    "Drainage basin",
    "Hyetograph",
    "Runoff",
    # "Infiltration",
    # "Rainfall-runoff models",
    "Design storm",
    "IDF curve",
    "~Oroville Dam",
    "~Watershed delimitation",
]


def page_week_08(option: TOC):
    st.title(option.replace("~", ""))

    if option == "Water cycle":
        img_url = "./book/assets/img/USGS_WaterCycle_English_ONLINE_20230302.png"
        source = "https://labs.waterdata.usgs.gov/visualizations/water-cycle/index.html#/"
        st.caption(
            rf"""
            **The Water Cycle** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.divider()
        img_url = "https://agupubs.onlinelibrary.wiley.com/cms/asset/23f15005-7268-47f1-bda1-4054ff85f657/eft21123-fig-0001-m.jpg"
        source = "https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021EF002613"

        st.caption(
            rf"""
            **A conceptual model** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

    elif option == "Drainage basin":
        st.header("Watersheds")

        img_url = "https://upload.wikimedia.org/wikipedia/commons/0/02/Amazonriverbasin_basemap.png"
        source = "https://commons.wikimedia.org/wiki/File:Amazonriverbasin_basemap.png"

        st.caption(
            rf"""
            **Amazon river basin** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        with st.expander(
            "Check **Hydrosheds**, global hydrography derived from spaceborne elevation data",
            expanded=True,
        ):
            img_url = "https://uploads-ssl.webflow.com/602ebbdd5021f30e81efbad9/62536860d9d1c6fe627d42ce_HydroSHEDS_zoom-p-1080.jpeg"
            source = "https://www.hydrosheds.org/products/hydrosheds"
            st.caption(
                rf"""
                **Amazon river basin** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

            st.divider()
            _, col, _ = st.columns([1, 10, 1])
            with col:
                url = "https://doi.org/10.1029/2008eo100001"
                st.markdown(
                    rf"""
                    Also check:

                    ⏺ Lehner, B., Verdin, K., & Jarvis, A. (2008). <br>
                    **New Global Hydrography Derived From Spaceborne Elevation Data**. <br>
                    *In Eos, Transactions American Geophysical Union (Vol. 89, Issue 10, p. 93)* <br>
                    DOI: [10.1029/2008eo100001]({url})
                    
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()
        img_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/WBD_Base_HUStructure_small.png"
        source = (
            "https://www.usgs.gov/media/images/watershed-boundary-dataset-structure-visualization"
        )
        st.caption(
            rf"""
            **Watershed Boundary Structure** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        img_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/WBD_SubRegions_24x18.png"
        source = "https://www.usgs.gov/media/images/watershed-boundary-dataset-subregions-map"

        st.caption(
            rf"""
            **Watershed Boundary Dataset Map** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.divider()
        st.header("Sewage systems")
        img_url = "./book/assets/img/sewer_system_map_Bogotá.png"
        source = "https://www.acueducto.com.co/wassigue6/MapasGeoportal"

        st.caption(
            rf"""
            **Map of sewer system in Bogotá (Colombia)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )

        st.image(img_url, use_container_width=True)

        st.divider()
        st.markdown("#### Combined v. separate sewer systems")

        cols = st.columns(2)

        with cols[0]:
            img_url = "https://i0.wp.com/civilengineerspk.com/wp-content/uploads/2014/03/002.jpg"
            source = "https://www.civilengineerspk.com/design-of-sewer-system/"

            st.markdown("**Dry weather**")
            st.caption(f":red[Dry weather] - Source: [{urlparse(source).hostname}]({source})")
            st.image(img_url, use_container_width=True)

        with cols[1]:
            img_url = "https://i0.wp.com/civilengineerspk.com/wp-content/uploads/2014/03/001.jpg"
            source = "https://www.civilengineerspk.com/design-of-sewer-system/"
            st.markdown("**Wet weather**")
            st.caption(f":blue[Wet weather] - Source: [{urlparse(source).hostname}]({source})")
            st.image(img_url, use_container_width=True)

    elif option == "Hyetograph":
        st.header("Hyetograph ↦ plot of rainfall intensity over time")

        st.info(
            r"""
            Gather data from the USGS database on:
            - https://help.waterdata.usgs.gov/faq/automated-retrievals
            - https://waterdata.usgs.gov/nwis/current/?type=precip&group_key=state_cd
            """
        )

        # rain = get_hydrologic_data()
        # st.dataframe(rain)
        # rain["per-hour"] = rain["value"].rolling(12, center=False).sum()

        # figs = dict()

        # figs["raw"] = go.Figure([go.Bar(x=rain["dateTime"], y=rain["value"])])

        # figs["per-hour"] = go.Figure([go.Bar(x=rain["dateTime"], y=rain["per-hour"])])

        # titles = ["Total rainfall in 5 min [in]", "Rainfall intensity [in/hr]"]
        # for t, fig in zip(titles, figs.values()):
        #     fig.update_layout(
        #         title_text="""Data from a USGS rain gauge. <br>Source <a href="https://waterdata.usgs.gov/monitoring-location/414542087380901/#parameterCode=00045&period=P30D">Waterdata - USGS</a>""",
        #         height=500,
        #         yaxis=dict(title=t, **axis_format),
        #         xaxis=dict(title="Datetime", **axis_format),
        #         hovermode="closest",
        #         hoverlabel=dict(font_size=18),
        #     )

        # tabs = st.tabs(["Raw data", "Aggregated per hour"])

        # for tab, fig in zip(tabs, figs.values()):
        #     with tab:
        #         st.plotly_chart(fig, use_container_width=True)

        # "*****"
        # cols = st.columns([1, 2])
        # with cols[0]:
        #     "&nbsp;\n\n&nbsp;\n\n"
        #     st.info("What is an inch of rain?")

        # with cols[1]:
        #     img_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/wss-rain-storm-colorado.jpg"
        #     source = "https://www.usgs.gov/media/images/rainstorms-can-be-localized-or-widespread"

        #     st.caption(
        #         rf"""
        #         **A localized heavy summer rainstorm in Colorado** <br>
        #         Source: [{urlparse(source).hostname}]({source})
        #         """,
        #         unsafe_allow_html=True,
        #     )
        #     st.image(img_url, use_container_width=True)

        r"""
        ******
        ### How is rainfall measured? &nbsp; ↝  &nbsp; The tipping bucket rain gauge
        """

        cols = st.columns(4)

        with cols[0]:
            img_url = (
                "https://upload.wikimedia.org/wikipedia/commons/4/42/Exterior_tipping_bucket.JPG"
            )
            source = (
                "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Exterior_tipping_bucket.JPG"
            )
            st.caption(
                rf"""
                **Exterior** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        with cols[1]:
            img_url = (
                "https://upload.wikimedia.org/wikipedia/commons/9/90/Interior_tipping_bucket.JPG"
            )
            source = (
                "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Interior_tipping_bucket.JPG"
            )
            st.caption(
                rf"""
                **Interior** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        with cols[2]:
            img_url = (
                "https://upload.wikimedia.org/wikipedia/commons/6/67/Tipping_Bucket_Recorder.JPG"
            )
            source = (
                "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Tipping_Bucket_Recorder.JPG"
            )
            st.caption(
                rf"""
                **Recording** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        with cols[3]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/f/fd/Close_up_chart.JPG"
            source = "https://en.wikipedia.org/wiki/Rain_gauge#/media/File:Close_up_chart.JPG"
            st.caption(
                rf"""
                **Close-up** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        "******"

        cols = st.columns([1, 3])
        with cols[0]:
            "&nbsp;"
            "&nbsp;"

            year = st.select_slider("Year", range(2000, 2024, 1), 2022)
            month = st.select_slider("Month", range(1, 13, 1), 12)
            which = st.selectbox("Map", ["Monthly total", "Deviation from average"])
        with cols[1]:
            source = "https://www.climate.gov/maps-data/data-snapshots/snapshot?id=8701"

            if which == "Monthly total":
                img_url = f"https://www.climate.gov/data/Precipitation--Monthly--Total--CONUS/02-large/Precipitation--Monthly--Total--CONUS--{year}-{month:02d}-00--large.png"

                st.caption(
                    rf"""
                    **Monthly total precipitation** <br>
                    Source: [{urlparse(source).hostname}]({source})
                    """,
                    unsafe_allow_html=True,
                )
            elif which == "Deviation from average":
                img_url = f"https://www.climate.gov/data/Precipitation--Monthly--Difference-from-average--CONUS/02-large/Precipitation--Monthly--Difference-from-average--CONUS--{year}-{month:02d}-00--large.png"

                st.caption(
                    rf"""
                    **Monthly difference from average** <br>
                    Source: [{urlparse(source).hostname}]({source})
                    """,
                    unsafe_allow_html=True,
                )

            st.image(img_url, use_container_width=True)

    elif option == "Runoff":
        r"""
        ## Hydrograph ↦ plot of discharge over time
        """

        flow = get_hydrologic_data()
        fig = go.Figure([go.Scatter(x=flow.index, y=flow["00065_Mean"])])

        fig.update_layout(
            title_text="""Data from a USGS station. <br>Source <a href="https://waterdata.usgs.gov/monitoring-location/02223500/#parameterCode=00065&period=P30D">Waterdata - USGS</a>""",
            height=500,
            yaxis=dict(title="Streamflow [ft³/s]", **axis_format),
            xaxis=dict(title="Datetime", **axis_format),
            hovermode="closest",
            hoverlabel=dict(font_size=18),
        )

        st.plotly_chart(fig, use_container_width=True)

        "*****"
        st.info("How are rain and runoff related?")
        cols = st.columns([1, 2])
        with cols[0]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/8/80/Surface_water_cycle.svg"
            source = "https://en.wikipedia.org/wiki/Runoff_model_(reservoir)"

            st.caption(
                rf"""
                **Runoff from the water balance** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        with cols[1]:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/9/95/Runoff_of_soil_%26_fertilizer.jpg"
            source = "https://commons.wikimedia.org/wiki/File:Runoff_of_soil_&_fertilizer.jpg"

            st.caption(
                rf"""
                **Runoff from a farm field in Iowa** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

    elif option == "Design storm":
        st.markdown(
            R"""
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
        )

        url = "https://jeffskwang.github.io/"
        st.link_button("⛈️ Go to rain/runoff example", url, use_container_width=True, type="primary")

        st.markdown(
            R"""
            *****
            ### Synthetic Block design-storm hyetograph

            - From a IDF curve, identify the return period and duration. The design
            storm will contain the intensities related to all the durations less than
            the duration design. 
            
            - $\Delta t$ should not be greater than the time of concentration

            - The peak intensity of the storm is usually placed between 1/3 and 1/2 the
            duration of the storm. 
            
            *****
            ### Soil Conservation Service hyetographs

            Developed for 24-hr storms

            From the Urban Hydrology for Small Watersheds -
            USDA - Natural Resources Conservation Service -
            TR-55 (June 1986): 

            > The length of the most intense rainfall period contrib-
            > uting to the peak runoff rate is related to the time of
            > concentration for the watershed. In a hydrograph
            > created with NRCS procedures, the duration of rainfall
            > that directly contributes to the peak is about 170
            > percent of the time of concentration. 

            > - Types I and IA represent the Pacific maritime climate
            > with wet winters and dry summers. 
            > - Type III represents Gulf of Mexico and Atlantic coastal 
            > areas where tropical storms bring large 24-hour rainfall amounts. 
            > - Type II represents the rest of the country. 
            > 
            > *For more precise distribution boundaries in a state having more than*
            > *one type, contact the NRCS State Conservation Engineer*
            
            """
        )

        st.caption("SCS 24-HR Rainfall distributions")
        cols = st.columns([1, 1.5])
        with cols[0]:
            scs = pd.read_excel("./book/assets/tables/SCS_24HR_RainfallDistribution.xlsx")
            st.dataframe(scs, use_container_width=True, height=300)

        with cols[1]:
            fig, ax = plt.subplots()
            colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
            for c, t in zip(colors, ["I", "IA", "II", "III"]):
                ls = "dotted" if t == "III" else "-"
                ax.plot("t(hr)", f"Type {t}", data=scs, c=c, lw=3, ls=ls)

            ax.legend()
            ax.set_xlabel("Time [hr]")
            ax.set_ylabel("Fraction of 24-hr rainfall $P/P_T$")
            ax.grid(True)
            ax.set_ylim(0, 1)
            ax.set_xlim(0, 24)
            ax.xaxis.set_major_locator(MultipleLocator(4))
            st.pyplot(fig, use_container_width=True)

        source = "https://directives.sc.egov.usda.gov/22162.wba"
        st.caption(
            rf"""
            Source: Urban Hydrology for Small Watersheds <br>
            USDA - Natural Resources Conservation Service <br>
            [Technical Release TR-55 (June 1986)]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image("./book/assets/img/SCS_24hr_Map.png")

        st.warning(
            "The Soil Conservation Service is now called the Natural Resources Conservation Service (NRCS)"
        )

    elif option == "IDF curve":
        st.markdown(
            R"""
            ## IDF: Intensity-Duration-Frequency curves

            $$
                \textsf{Empirical:} \quad I(t) = \dfrac{a}{\left( t + c \right)^n}
            $$
            """
        )

        cols = st.columns([3, 1])
        with cols[0]:
            st.image("./book/assets/img/IDF curve Ohare IL.png", use_container_width=True)
        with cols[1]:
            source = "https://hdsc.nws.noaa.gov/hdsc/pfds/pfds_map_cont.html"
            st.caption(
                rf"""
                &nbsp;

                &nbsp;

                Source: NOAA's National Weather Service <br>
                [Precipitation Frequency Data Server (PFDS)]({source})""",
                unsafe_allow_html=True,
            )
            st.image("./book/assets/img/yrs_legend_pds.png")

        # cols = st.columns([2,2])
        # with cols[0]:
        #     st.map({"LAT":[42.0660], "LON":[-87.7332]}, zoom=4, use_container_width=True)
        # with cols[1]:
        #     st.image("https://hdsc.nws.noaa.gov/hdsc/pfds/plots/42.0660_-87.7332_ams_IDF_in_ari.png", use_container_width=True)

        url = "https://hdsc.nws.noaa.gov/hdsc/pfds/pfds_map_cont.html"
        st.link_button(
            "Go to NOAA Precipitation Frequency Data Server",
            url,
            use_container_width=True,
            type="primary",
        )

    elif option == "~Oroville Dam":
        oroville_dam()

    elif option == "~Watershed delimitation":
        watershed_delimitation()

    else:
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"


def open_page(url):
    open_script = f"""
        <script type="text/javascript">
            window.open('{url}', '_blank').focus();
        </script>
    """
    st.html(open_script)


@st.cache_data
def get_hydrologic_data(dummy: str = "dummy"):
    df, _ = get_dv(sites=["02223500"], start="2023-03-13", end="2023-04-12")
    return df


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
#         st.image(img_url, use_container_width=True)

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
#         st.image(img_url, use_container_width=True)
