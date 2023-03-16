import streamlit as st
import plotly.graph_objects as go
import numpy as np
from itertools import cycle

st.set_page_config(layout='wide')

with open("assets/style.css") as f:
    st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

#####################################################################

st.title("CIV-ENV 340: Hydraulics and hydrology")
"****"

with st.sidebar:
    lottie = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player src="https://assets4.lottiefiles.com/private_files/lf30_nep75hmm.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
    """
    st.components.v1.html(lottie, width=200, height=100)

    "## Week 9"
    "### Select a topic:"
    option = st.radio("Select a topic:",
        [],
        label_visibility="collapsed")
    
    "***"
    st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
    
    r"""
    #### Class textbook:
    [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
    Pearson Education Inc., Boston.
    """

####################################################################
    
if option == "":
    r" ### 🚧 Under construction 🚧"

else: 
    st.error("You should not be here!")
    r" ### 🚧 Under construction 🚧"