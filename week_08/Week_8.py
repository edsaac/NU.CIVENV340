import streamlit as st
import pickle
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

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
        ## Culvert

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
        ## Hyetograph
        """
        
        cols = st.columns(2)

        with cols[0]:
            r"""
            Plot of rainfall intensity over time
            """


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

    elif option == "Runoff":
        r"""
        ## Hydrograph
        """
        
        cols = st.columns(2)

        with cols[0]:
            r"""
            Plot of runoff volume over time
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

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

if __name__ == "__main__":
    main()