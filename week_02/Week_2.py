import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout='wide')

st.markdown("""
<style>

tr .math {
    font-size: 0.8rem;
}

table {
  margin-left: auto;
  margin-right: auto;
}

[data-testid="stCaptionContainer"] {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

h1 {
    font-size: 2rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("CIV-ENV 340: Hydraulics and hydrology")
"****"

with st.sidebar:
    lottie = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player src="https://assets4.lottiefiles.com/private_files/lf30_nep75hmm.json"  background="transparent"  speed="2"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
    """
    st.components.v1.html(lottie, width=310, height=100)
    
    "## Week 2"
    "### Select a topic:"
    option = st.radio("Select a topic:",
        ["Friction head loss", "Empirical relationships", "Equations summary", "Accessories", "Momentum and forces"],
        label_visibility="collapsed")
    r"""
    ***
    ### Class textbook:
    """
    cols = st.columns([1,2])
    with cols[0]: st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
    with cols[1]: 
        r"""[🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, et al.*, **Fundamentals of hydraulic engineering systems** Fifth edition (2017),
        Boston. Pearson.
        """
    
if option == "Friction head loss":

    r"""

    ## Head loss due friction $h_f$

    **Darcy-Weisbach equation:**
    
    $$
        h_f = f \left( \dfrac{L}{D}\right) \dfrac{V^2}{2g}
    $$

    |Parameter|Description|Units|
    |:---:|:---|:---:|
    |$f$| Friction factor | $ - $|
    |$L$| Pipe length | ${\rm m}$ |
    |$D$| Pipe diameter | ${\rm m}$|
    |$V/2g$| Velocity head | ${\rm m}$|
    
    &nbsp;
    """

    st.warning("Is Darcy-Weisbach equation dimensionally homogeneous?")

    r"""
    In terms of discharge: 

    $$
        h_f = f \left( \dfrac{L}{D} \right) \dfrac{8Q^2}{\pi^2 D^4 g}
    $$


    In general:

    $$
        h_f = KQ^m
    $$

    |Parameter|Description|Units|
    |:---:|:---:|:---:|
    |$K$| ⁉️ | ❓ |
    |$m$| ⁉️ | ❓ |

    ****
    ## Friction factor $f$
    """

    tabs = st.tabs(["Laminar flow", "Turbulent flow"])    
    
    with tabs[0]:
        r"""
        **Hagen-Poiseuille law:**
        
        $$
            f = \dfrac{64}{R_e}
        $$

        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$R_e$| Reynolds number | $ - $|
        """
    
    with tabs[1]:
        r"""
        **Colebrook-White equation:**
        
        $$
            \dfrac{1}{\sqrt{f}} = -\log\left( \dfrac{e}{3.7\,D} + \dfrac{2.51}{R_e \, \sqrt{f}} \right)
        $$
        
        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$e$| Roughness height | $ {\rm m} $|
        |$e/D$| Relative roughness | $ - $
        |$D$| Pipe diameter | ${\rm m}$|
        |$R_e$| Reynolds number | $ - $|
        """

        r"""
        &nbsp;

        **Swamme-Jain equation:**

        $$
            f = \dfrac{0.25}{\left[ \log{\left( \dfrac{e}{3.7\,D} + \dfrac{5.74}{R_e^{0.9}} \right)} \right]^2}
        $$

        """

        st.warning("How close is the Swamme-Jain equation to the implicit Colebrook-White equation?")

    r"""
    ****
    ## Moody diagram
    """

    st.image("https://upload.wikimedia.org/wikipedia/commons/d/d9/Moody_EN.svg", use_column_width=True)
    st.caption("*Source* [🛸](https://commons.wikimedia.org/wiki/File:Moody_EN.svg)")

elif option == "Empirical relationships":

    r"""
    ## Hazen-Williams equation
    """

elif option == "Equations summary":

    r"""
    
    $$
        h_f = KQ^m
    $$

    |Equation|m|K (BG System)|K (SI System) |
    |:---:|:---:|:---:|:---:|
    |Darcy-Weisbach (Turbulent flow)| $2.0$ | $\dfrac{0.0252fL}{D^5}$ | $\dfrac{0.0826fL}{D^5}$ |
    |Hazen-Williams                 | $1.85$ | $\dfrac{4.73L}{D^{4.87}C^{1.85}_{\texttt{HW}}}$ | $\dfrac{10.7L}{D^{4.87}C^{1.85}_{\texttt{HW}}}$ |
    |Manning  | $2.0$ | $\dfrac{4.64n^2L}{D^{5.33}}$ | $\dfrac{10.3n^2L}{D^{5.33}}$ |
    

    """

    st.caption("*Source:* Table 3.4 - Course textbook")

elif option == "Accessories":

    r"""
    ## Pipe accessories
    """

    r"""
    ****
    ## Head loss in accessories $h_a$
    """

elif option == "Momentum and forces":
    r"""
    ## Momentum balance
    """

else: 
    st.error("You should not be here!")