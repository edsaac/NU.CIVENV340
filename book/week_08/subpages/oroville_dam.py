import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse


def oroville_dam():
    st.markdown(
        R"""
        ## Case study - Oroville Dam (Feb/2017)
        
        ### Location
        """
    )
    coords_oroville = {"LAT": [39.540393440305344], "LON": [-121.48272756529394]}
    st.map(coords_oroville, zoom=10, use_container_width=True)

    st.markdown(
        R"""
        ****
        ### Crisis
        """
    )

    html(
        R""" <iframe src="https://commons.wikimedia.org/wiki/File:Lake_Oroville_Spillways_February_12,_2017.webm?embedplayer=yes" width="100%" height="400" frameborder="0" ></iframe>""",
        height=450,
        scrolling=True,
    )

    url = "https://en.wikipedia.org/wiki/Oroville_Dam_crisis"
    st.caption(
        rf"""
        ******
        **Timeline of Oroville Dam crisis** <br>
        Source: [{urlparse(url).hostname}]({url})""",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            "🌊 Normal operation",
            "💸 Upgrade",
            "🏄‍♀️ Main spillway fail",
            "🪨 Emergency spillway",
            "🛠️ Repairs",
            "🚧 Risks",
        ]
    )
    urls = [
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/OROVILLE_DAM_1.svg",
        "https://upload.wikimedia.org/wikipedia/commons/a/ae/OROVILLE_DAM_2.svg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f7/OROVILLE_DAM_3.svg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d5/OROVILLE_DAM_4.svg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b7/OROVILLE_DAM_5.svg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c4/OROVILLE_DAM_6.svg",
    ]

    for tab, url in zip(tabs, urls):
        with tab:
            _, col, _ = st.columns([1, 2, 1])
            with col:
                st.image(url, use_column_width=True)

    st.markdown(
        R"""
        ****
        ### Spillway failure
        """
    )

    imgs = [
        "https://upload.wikimedia.org/wikipedia/commons/b/b3/Oroville_Dam_main_spillway_30_March_2011.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/Oroville_Dam_spillway_damage_7_Feb_2017-10235.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b3/Oroville_Dam_spillway_damage_February_27_2017.jpg",
    ]

    cols = st.columns(3)

    for img, col in zip(imgs, cols):
        with col:
            st.image(img, use_column_width=True)

    st.divider()

    with st.expander("**Infographic**", expanded=True):
        source = "https://cdec.water.ca.gov/reservoir.html"
        img = "https://upload.wikimedia.org/wikipedia/commons/9/92/Lake_Oroville_events_timeline.jpg"

        st.markdown(
            R"""
            Lake Oroville Spillway Incident: Timeline of major events February 4-25
            Source
            """
            + f"Source: [{urlparse(source).hostname}]({source})",
            unsafe_allow_html=True,
        )

        st.image(img, use_column_width=True)

    st.markdown(
        R"""
        ****
        ### Other stuff
        """
    )

    cols = st.columns(2)

    with cols[0]:
        img = "https://www.fema.gov/sites/default/files/photos/fema_ndsasd.png"
        source = "https://www.fema.gov"

        st.caption(
            R"""
            **National Dam Safety day**<br>
            """
            + f"Source: [{urlparse(source).hostname}]({source})",
            unsafe_allow_html=True,
        )

        st.image(img, use_column_width=True)

    with cols[1]:
        img = "https://nid.sec.usace.army.mil/assets/images/TieHack2018WY02030WYDamSafety.jpg"
        source = "https://nid.sec.usace.army.mil/"

        st.caption(
            R"""
            **National Inventory of Dams: more than 90.000 dams nation-wide**<br>
            """
            + f"Source: [{urlparse(source).hostname}]({source})",
            unsafe_allow_html=True,
        )

        lilcols = st.columns(3)
        st.image(img, use_column_width=True)

        with lilcols[0]:
            st.metric("Total Dams", "> 90,000")
        with lilcols[1]:
            st.metric("Avg. age", "61 years")
        with lilcols[2]:
            st.metric("with Hydropower", "3%")


if __name__ == "__main__":
    oroville_dam()
