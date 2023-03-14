import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout='centered')

st.markdown("""
<style>

tr .math {
    font-size: 0.8rem;
}

table {
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
    <lottie-player src="https://assets4.lottiefiles.com/packages/lf20_w9GTXN.json"  background="transparent"  speed="1"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
    """
    st.components.v1.html(lottie, width=310, height=100)

    "## Week 1"
    "### Select a topic:"
    option = st.radio("Select a topic:",
        ["System of units", "Water properties", "Fluid classification", "Pressure and head", "Mass & energy"],
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
    
if option == "System of units":

    tabs = st.tabs(["**Normal conditions**", "**Standard conditions**"])

    with tabs[0]:

        r"""

        | Parameter           | Symbol | Units       | SI                                | BG                                     |
        |:--------------------|:------:|:-----------:|:---------------------------------:|:--------------------------------------:|
        |Temperature          | $T$    | Temperature | $20.2 \, \degree\textrm{C}$       | $68.4 \, \degree\textrm{F}$            |
        |Atmospheric pressure | $p_{\rm atm}$    | Force/Area  | $1.014 \times 10^{5} \, \textrm{Pa}$ | $14.7 \, \textrm{lb}/\textrm{in}^2$ |
        |Atmospheric pressure | $p_{\rm atm}/\gamma$ | Lenght  | $10.3 \, \textrm{m H}_2\textrm{O}$   | $33.8 \, \textrm{ft H}_2\textrm{O}$ |
        |Gravitational acceleration| $g$ | Lenght/Time²  | $9.81 \, \textrm{m}/\textrm{s}^2$| $32.2 \, \textrm{ft}/\textrm{s}^2$ |
        """
        
        "****"

        r"""
        | Water property    | Symbol   | Units              | SI                                                 | BG                                                   |
        |:---------         |:--------:|:------------------:|:--------------------------------------------------:|:----------------------------------------------------:|
        |Specific weight    | $\gamma$ | Force/Lenght       | $9790                \, \textrm{N}/\textrm{m}^3$   | $62.3                \, \textrm{lb}/\textrm{ft}^3$   |
        |Density            | $\rho$   | Mass/Volume        | $998                 \, \textrm{kg}/\textrm{m}^3$  | $1.94                \, \textrm{slug}/\textrm{ft}^3$ |
        |Viscosity          | $\mu$    | Force · Time/Area  | $1.00 \times 10^{-3} \, \textrm{N s}/\textrm{m}^2$ | $2.09 \times 10^{-5} \, \textrm{lb s}/\textrm{ft}^2$ |
        |Kinematic viscosity| $\nu$    | Area/Time          | $1.00 \times 10^{-6} \, \textrm{m}^2/\textrm{s}$   | $1.08 \times 10^{-5} \, \textrm{ft}^2/\textrm{s}$    |
        |Surface tension    | $\sigma$ | Force/Lenght       | $7.13 \times 10^{-2} \, \textrm{N}/\textrm{m}$     | $4.89 \times 10^{-3} \, \textrm{lb}/\textrm{ft}^{-3}$|
        |Vapor pressure     |   -      | Force/Area         | $2.37 \times 10^{3}  \, \textrm{N}/\textrm{m}^2$   | $3.44 \times 10^{-1} \, \textrm{lb}/\textrm{in}^2$   |
        """
    
    with tabs[1]:

        r"""
        | Condition           | Symbol | Units       | SI                                | BG                                     |
        |:--------------------|:------:|:-----------:|:---------------------------------:|:--------------------------------------:|
        |Temperature          | $T$    | Temperature | $4 \, \degree\textrm{C}$       | $68.4 \, \degree\textrm{F}$            |
        |Atmospheric pressure | $p_{\rm atm}$    | Force/Area  | $1.014 \times 10^{5} \, \textrm{Pa}$ | $14.7 \, \textrm{lb}/\textrm{in}^2$ |
        |Atmospheric pressure | $p_{\rm atm}/\gamma$ | Lenght  | ❓   | ❓ |
        |Gravitational acceleration| $g$ | Lenght/Time²  | $9.81 \, \textrm{m}/\textrm{s}^2$| $32.2 \, \textrm{ft}/\textrm{s}^2$ |
        """
        
        "****"

        r"""

        | Water property    | Symbol   | Units              | SI                                                 | BG                                                   |
        |:---------         |:--------:|:------------------:|:--------------------------------------------------:|:----------------------------------------------------:|
        |Specific weight    | $\gamma$ | Force/Lenght       | $9810                \, \textrm{N}/\textrm{m}^3$   | $62.4                \, \textrm{lb}/\textrm{ft}^3$   |
        |Density            | $\rho$   | Mass/Volume        | $1000                 \, \textrm{kg}/\textrm{m}^3$ | $1.94                \, \textrm{slug}/\textrm{ft}^3$ |
        |Viscosity          | $\mu$    | Force · Time/Area  | $1.57 \times 10^{-3} \, \textrm{N s}/\textrm{m}^2$ | $3.28 \times 10^{-5} \, \textrm{lb s}/\textrm{ft}^2$ |
        |Kinematic viscosity| $\nu$    | Area/Time          | $1.57 \times 10^{-6} \, \textrm{m}^2/\textrm{s}$   | $1.69 \times 10^{-5} \, \textrm{ft}^2/\textrm{s}$    |
        |Surface tension    | $\sigma$ | Force/Lenght       | $7.36 \times 10^{-2} \, \textrm{N}/\textrm{m}$     | $5.04 \times 10^{-3} \, \textrm{lb}/\textrm{ft}^{-3}$|
        |Vapor pressure     |   -      | Force/Area         | $8.21 \times 10^{2}  \, \textrm{N}/\textrm{m}^2$   | $1.19 \times 10^{-1} \, \textrm{lb}/\textrm{in}^2$   |
        """

elif option == "Water properties":

    r"""
    ## Density $\rho_{(T)}$
    """

    density = pd.read_excel("week_01/properties.xlsx", sheet_name="Density_water")
    density["Density (kg/m3)"] = density["Density (g/cm3)"] * 1.0e3

    fig = go.Figure([
        go.Scatter(
            x=density['Temperature (C)'], 
            y=density['Density (kg/m3)'],
            name="Water density",
            hovertemplate="T = %{x} °C <br><b>ρ = %{y} kg/m³</b>",
            line=dict(
                width=5, 
                color="#018749")
        )
    ])

    fig.update_layout(
        title_text = '''Standard Density of Water as a Function of Temperature<br><i>Data retrieved from the <a href="https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9982163963102441">CRC Handbook of Chemistry and Physics Online</a></i>''',
        yaxis=dict(
            title="Density [kg/m³]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        xaxis=dict(
            title="Temperature [°C]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
    )

    st.plotly_chart(fig, use_container_width=True)

    r"""
    ****
    ## Dynamic Viscosity $\mu_{(T)}$
    """

    viscosity = pd.read_excel("week_01/properties.xlsx", sheet_name="Viscosity")
    viscosity["Water viscosity (μ) [SI]"] = viscosity["Water viscosity (μ) [SI]"] * 1e-3  # Convert to N.s/m²
    viscosity["Air viscosity (μ) [SI]"] = viscosity["Air viscosity (μ) [SI]"] * 1e-5  # Convert to N.s/m²

    fig = go.Figure([
        go.Scatter(
            x=viscosity["Temp (C)"],
            y=viscosity["Water viscosity (μ) [SI]"],
            name="Water",
            hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
            line=dict(
                width=2, 
                color="blue"),
            marker=dict(
                size=6
            )
        ),
        go.Scatter(
            x=viscosity["Temp (C)"],
            y=viscosity["Air viscosity (μ) [SI]"],
            name="Air",
            hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
            line=dict(
                width=2, 
                color="red"),
            marker=dict(
                size=6
            )
        )
    ])

    fig.update_layout(
        height=700,
        title=dict(
            text='''Viscosities of water and air<br><i>Data retrieved from Table 1.3 - <i>Class textbook</i>''',
            font_color="#444"),
        yaxis=dict(
            title="Viscosity [N.s/m²]",
            type="log",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        xaxis=dict(
            title="Temperature [°C]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        legend=dict(
            title="Fluid",
            orientation="v",
            bordercolor="gainsboro",
            borderwidth=1,
            yanchor="bottom", y=0.90,
            xanchor="center", x=0.50
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
    """
    - What is a `poise`? 
    - Who was JLM Poiseuille? 🇫🇷
    """)

    r"""
    ****
    ## Kinematic Viscosity $\nu_{(T)}$

    $$
        \nu = \dfrac{\mu}{\rho}
    $$

    """

    viscosity = pd.read_excel("week_01/properties.xlsx", sheet_name="Viscosity")
    viscosity["Kinematic water viscosity (ν) [SI]"] = viscosity["Kinematic water viscosity (ν) [SI]"] * 1e-6  # Convert to N.s/m²
    viscosity["Kinematic air viscosity (ν) [SI]"] = viscosity["Kinematic air viscosity (ν) [SI]"] * 1e-6  # Convert to N.s/m²

    fig = go.Figure([
        go.Scatter(
            x=viscosity["Temp (C)"],
            y=viscosity["Kinematic water viscosity (ν) [SI]"],
            name="Water",
            hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
            line=dict(
                width=2, 
                color="blue"),
            marker=dict(
                size=6
            )
        ),
        go.Scatter(
            x=viscosity["Temp (C)"],
            y=viscosity["Kinematic air viscosity (ν) [SI]"],
            name="Air",
            hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
            line=dict(
                width=2, 
                color="red"),
            marker=dict(
                size=6
            )
        )
    ])

    fig.update_layout(
        height=700,
        title=dict(
            text='''Viscosities of water and air<br><i>Data retrieved from Table 1.3 - <i>Class textbook</i>''',
            font_color="#444"),
        yaxis=dict(
            title="Kinematic viscosity [m²/s]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        xaxis=dict(
            title="Temperature [°C]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        legend=dict(
            title="Fluid",
            orientation="v",
            bordercolor="gainsboro",
            borderwidth=1,
            yanchor="bottom", y=0.90,
            xanchor="center", x=0.50
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
    """
    - What is a `stokes`? 
    - Who was GG Stoke? 🇬🇧 
    """)

elif option == "Fluid classification":

    r"""
    ## Fluids

    ### Compressible | Non-compressible

    Does the fluid density depend on pressure?
    

    ### Newtonian | Non-newtonian

    Does the fluid viscosity depend on the shear stress?

    """

    r"""
    *****
    ## Flows

    ### Permanent/Transient

    Does the flow change over time?
    

    ### Uniform/Varied

    Does the flow change over space?

    ### Turbulent/Laminar

    Are viscous stresses dominant over the flow inertia?

    **Reynolds number:**
    $$
        R_e = \dfrac{\textrm{Inertial forces}}{\textrm{Viscous forces}} = \dfrac{uL}{\nu}
    $$

    ### Subcritical/supercritical

    Are body forces dominant over the flow inertia?

    **Froude number:**
    $$
        F_r = \dfrac{\textrm{Inertial forces}}{\textrm{Body forces}} = \dfrac{u}{\sqrt{gL}}
    $$

    """

elif option == "Pressure and head":
    r"""
    ## Absolute and gauge pressure

    $$
        p = p_{\rm abs} - p_{\rm atm}
    $$

    """

    with st.expander("**Diagram:**"):
        st.image("https://www.engineeringtoolbox.com/docs/documents/587/absolute_gauge_pressure.png", use_column_width=True)
        st.caption("*Source* [🛸](https://www.engineeringtoolbox.com/docs/documents/587/absolute_gauge_pressure.png)")

    r"""
    ### Barometric formula

    $$
        \dfrac{p_{\rm atm}}{p_{\rm atm, 0}} \approx \exp\left( - \dfrac{ghM}{T_0 R_0} \right) 
    $$
    
    &nbsp;
    
    |Parameter|Description|Value|
    |:---:|:---|---:|
    |$p_{\rm atm,0}$| Sea level standard atmospheric pressure| $101325 \, {\rm Pa}$|
    |$h$| Elevation above sea level | ${\rm m}$|
    |$M$| Molar mass of dry air | $0.02897 \, {\rm kg/mol}$|
    |$T_0$| Standard temperature | $288.16 \, {\rm K}$|
    |$R_0$| Ideal gas constant   | $8.314 \, {\rm J/mol.K}$|
    |$g$| Grav. acceleration   | $9.81 \, {\rm m/s²}$|
    
    &nbsp;
    """

    st.warning("Is this equation **dimensionally homogeneous**?")

    fig = go.Figure([
        go.Scatter(
            x=(height := np.linspace(0,4000,100)), 
            y=10.3 * np.exp(-(9.81*height*0.02897)/(288.16*8.314)),
            name="Barometric formula",
            hovertemplate="z = %{x:.1f} m <br><b>h = %{y:.2f} m H<sub>2</sub>O</b>",
            line=dict(
                width=5, 
                color="#018749")
        )
    ])

    fig.update_layout(
        title_text = '''Barometric formula<br><i><a href="https://en.wikipedia.org/wiki/Atmospheric_pressure">Source 📖</a></i>''',
        yaxis=dict(
            title="Atmospheric pressure [m H<sub>2</sub>O]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
        xaxis=dict(
            title="Elevation above sea level [m]",
            type="linear",
            showline=True,
            color="RGBA(1, 135, 73, 0.3)",
            tickcolor="RGBA(1, 135, 73, 0.3)",
            showgrid=True,
            griddash="dash",
            linewidth=1,
            gridcolor="RGBA(1, 135, 73, 0.3)"),
    )

    st.plotly_chart(fig, use_container_width=True)

    r"""

    ### Pressure and head

    $$
        h = \dfrac{p}{\gamma} = \dfrac{p}{\rho g}
    $$ 

    """

    r"""
    *****
    ## Hydrostatic pressure distribution

    $$
        p = \rho g \overbrace{y}^{\textrm{Depth}}
    $$ 

    """

    st.info(
        """
        - What are the center of gravity (CG) and the center of pressure (CP) on a surface?
        - Check Problem 2.5.2
        """
    )

elif option == "Mass & energy":
    
    r"""

    ## Flow rate and mean velocity

    $$ 
        Q = V\,A 
    $$

    |Parameter|Description|Units|
    |:---:|:---|---:|
    |$Q$| Discharge (volumetric flow rate) | ${\rm m³/s}$|
    |$V$| Mean velocity | ${\rm m/s}$|
    |$A$| Cross-sectional area | ${\rm m²}$|
    
    &nbsp;

    ## Reynolds number $R_e$

    $$
        R_e = \dfrac{uL}{\nu} = \underbrace{\dfrac{VD}{\nu}}_{\textsf{For circular pipes}}
    $$
    
    """

    with st.expander("Reynolds experiment"):
        st.video("https://www.youtube.com/watch?v=y0WRJtXvpSo")

    r"""
    ******
    ## Mass and energy conservations

    The discharge between two sections in a pipe must be the same

    $$
        Q_1 = Q_2
    $$
    
    The *Bernoulli's equation* describes the energy (head) balance of an ideal flow with no energy losses between
    two sections 

    $$
        H_1 = H_2
    $$

    But to account for energy losses, a head loss $h_L$ is introduced in the energy balance

    $$
        H_1 = H_2 + h_L
    $$

    Total energy is composed by potential, kinetic and pressure components, thus

    $$
        h_1 + \dfrac{p_1}{\gamma} + \dfrac{V_1^2}{2g} = h_2 + \dfrac{p_2}{\gamma} + \dfrac{V_2^2}{2g} + h_L
    $$
    
    &nbsp;

    |Parameter|Description|Units|
    |:---:|:---|:---:|
    |$H$| Total head | ${\rm m}$|
    |$h$| Elevation head | ${\rm m}$|
    |$p/\gamma$| Pressure head | ${\rm m}$|
    |$V/2g$| Velocity head | ${\rm m}$|

    &nbsp;

    For a pipe with a uniform size $V_1 = V_2$

    $$
        h_1 + \dfrac{p_1}{\gamma} = h_2 + \dfrac{p_2}{\gamma} + h_L
    $$

    """

    with st.expander("**Energy grade line (EGH)** and **hydraulic grade line (HGL)**"):
        st.image("https://www.pipeflow.com/public/PipeFlowExpertSoftwareHelp/desktop/PipeFlowExpertUserGuide_files/image371.jpg", use_column_width=True)
        st.caption("*Source* [🛸](https://www.pipeflow.com/public/PipeFlowExpertSoftwareHelp/desktop/Energy_and_Hydraulic_Grade_Lines.htm)")

else: 
    st.error("You should not be here!")