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
    <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ziet9v0c.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
    """
    st.components.v1.html(lottie, width=200, height=200)

    "## Week 3"
    "### Select a topic:"
    option = st.radio("Select a topic:",
        ["Pipes in series/parallel", "Pipe networks", "System of equations", "Newton method"],
        label_visibility="collapsed")
    
    "***"
    st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
    
    r"""
    #### Class textbook:
    [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
    Pearson Education Inc., Boston.
    """

####################################################################
    
if option == "Pipes in series/parallel":
    
    cols = st.columns(2)

    with cols[0]:
        r""" 
        ## Pipes in series

        The mass between consecutive pipes must be conserved,
        $$
            Q_1 = Q_2 = \mathellipsis  = Q_n
        $$

        Whereas the head loss adds up
        $$
            h_{L} = h_{L_1} + h_{L_2} + \mathellipsis + h_{L_n}
        $$
        
        """

    with cols[1]:
        r""" 
        ## Pipes in parallel
        
        The mass between the parallel pipes must be conserved,
        $$
            h_1 = h_2 = \mathellipsis = h_{L_n}
        $$

        Whereas the discharge adds up
        $$
            Q = Q_{1} + Q_{2} + \mathellipsis + Q_{n}
        $$
        
        """

elif option == "Pipe networks":
    r" ### 🚧 Under construction 🚧"
    r"""
    ## Branched networks


    ****
    ## Looped networks

    
    """

elif option == "System of equations":
    r" ### 🚧 Under construction 🚧"

elif option == "Newton method":
    r" ### 🚧 Under construction 🚧"

else: 
    r" ### 🚧 Under construction 🚧"