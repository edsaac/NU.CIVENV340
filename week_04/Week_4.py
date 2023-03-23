import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import plotly.graph_objects as go
import pickle, json
import numpy as np

from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    axis_format = dict(title_font_size=20,
        tickfont_size=16,
        showline=True,
        color="RGBA(1, 135, 73, 0.3)",
        tickcolor="RGBA(1, 135, 73, 0.3)",
        showgrid=True,
        griddash="dash",
        linewidth=1,
        gridcolor="RGBA(1, 135, 73, 0.3)")
    
    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_tuzu65Bu6N.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 150px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=150)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "System curve", 
                "Types of pumps", 
                "Characteristic curves", 
                "Cavitation", 
                "Pumps in series/parallel"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
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
    
    if option == "System curve":
        r"""
        ### System head curve
        """
        
        st.pyplot(pump_and_pipeline())

        r"""
        For the pump and pipeline system, a relationship for the head that the pump must provide can be derived 
        in terms of the static head plus the head losses due friction and accessories.

        $$
            H_A + \underbrace{H_p}_{\substack{\textsf{Head by} \\ \textsf{pump}}}= H_B + h_L
        $$

        $$
            H_p = \underbrace{(H_B - H_A)}_{\substack{\textsf{Static head}}} + h_L = H_\textsf{SH} + h_L
        $$
        
        $$
            H_p = H_\textsf{SH} + h_L
        $$

        Considering only friction losses (i.e., $h_L = h_f$)
        
        $$
            H_p = H_\textsf{SH} + KQ^m
        $$

        *****

        """
        cols = st.columns([0.8,1.4], gap="large")
        
        with cols[0]:
            diameter = st.slider("Diameter -- $D$ [m]", 0.01, 1.00, 0.61, step=0.01)

            length = st.slider("Pipe length -- $L$ [m]", 1.0, 1000.0, 100.0, step=1.0)

            rough_db = get_roughness_database()
            material = st.selectbox("Pipe material", rough_db.keys(), index=11)
            roughness = rough_db.get(material) * 1.0e-3  #Convert to meters
            st.metric("Roughness $e$", f"{roughness:.2E} m")
            
            rel_roughness = roughness/diameter
            st.metric("Rel. roughness $e/D$", f"{rel_roughness:.2E}")
            
            ν = st.number_input(r"Kinematic viscosity -- $\nu$ [m²/s]", 1e-7, 1e-3, 1e-6, format="%.2e")

            static_head = st.slider("Tank elevations -- $H_\mathsf{SH}$ [m]", -10.0, 90.0, (30.0, 67.0), step=1.0)
            H_static_head = static_head[1] - static_head[0]

            discharge = np.linspace(0.10, 2.0, 100)
            reynolds = 4.0 * discharge / (np.pi * diameter * ν)
            f = swamme_jain(rel_roughness, reynolds)
            hf = 0.0826 * f * length / np.power(diameter, 5) * np.power(discharge, 2)
            head_pump = H_static_head + hf

        with cols[1]:

            "### System curve ($Q$, $H_p$)"

            h_pump_fig = go.Figure([
                go.Scatter(
                    x = discharge,
                    y = head_pump,
                    name="System curve",
                    hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=5, 
                        color="#018749")
                )
            ])
            
            h_pump_fig.add_hline(
                y = H_static_head,
                name= "Static head",
                annotation=dict(
                    text="Static head",
                    font_size=19
                ),
                line=dict(
                        width=2,
                        dash="dashdot", 
                        color="#ff0044")
            )
            

            h_pump_fig.update_layout(
                height=650,
                margin=dict(t=40),
                #title_text = '''System curve''',
                yaxis=dict(
                    title="Head pump [m]",
                    range=[0,100],
                    **axis_format),
                xaxis=dict(
                    title="Discharge [m³/s]",
                    **axis_format),
                legend=dict(
                    title="Fluid",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top", y=0.96,
                    xanchor="right", x=0.96
                ),
                hoverlabel=dict(font_size=18),
            )
            
            st.plotly_chart(h_pump_fig, use_container_width=True)
    
        "****"

    elif option == "Types of pumps":
        r" ## Types of pumps"
        
        cols = st.columns(2)
        
        with cols[0]:
            "### Turbo-hydraulic pumps"
            
            with st.expander("🚁 **Centrifugal pumps**"):
                url = "https://www.lockewell.com/images/large/goulds/3656m_LRG.jpg"
                st.caption(f"Source: [lockwell.com]({url})")
                st.image(url, use_column_width=True)
                "*****"
                
                url = "https://en.wikipedia.org/wiki/Centrifugal_pump#/media/File:Centrifugal_Pump.png"
                st.caption("Source: [wikimedia.org]({url})")
                st.image("https://upload.wikimedia.org/wikipedia/commons/4/4a/Centrifugal_Pump.png", use_column_width=True)
                "*****"
                
                url = "https://www.youtube.com/watch?v=BaEHVpKc-1Q"
                st.caption(f"Source: [youtube.com/@Lesics]({url})")
                st.video(url)
            
            with st.expander("🦖 **Axial-flow (propeller) pumps**" ):
                url = "https://www.industrialchemicalpump.com/photo/pl23155791-single_stage_horizontal_axial_flow_pump_axially_split_impeller_centrifugal_pump.jpg"
                st.caption(f"Source: [industrialchemicalpump.com]({url})")
                st.image(url, use_column_width=True)
            

        with cols[1]:
            r"""
            ### Positive-displacement pumps
            """
            with st.expander("➰ **Rotary lobe pumps**" ):
                url = "https://www.youtube.com/watch?v=1ca-rXDqMMo"
                st.caption(f"Source: [youtube.com/@VikingPumpInc]({url})")
                st.video(url)
                "*****"

            with st.expander("➰ **Peristaltic pumps**" ):
                url = "https://www.youtube.com/watch?v=3H4Ftf_imrg"
                st.caption(f"Source: [youtube.com/@sityu82]({url})")
                st.video(url)
                "*****"

    elif option == "Characteristic curves":
        r" ## Characteristic curves"

        tabs = st.tabs(["**🌊 Pump head**", "**🦾 Efficiency**", "**🔋Power input**", "**🫧 NSPHr**"])

        discharge = np.linspace(0,500,100)
        system_head = 1e-4 * discharge**2 + 10.0

        with tabs[0]:  ## Head vs Q plot
            r"""
            **🌊 Pump head**

            $$
                H_p = a_0 + a_1 Q + a_2Q^2
            $$
            """
            cols = st.columns(3)
            with cols[0]: a0 = st.slider("$a_0$", 0.0, 100.0, 25.0)
            with cols[1]: a1 = st.slider("$a_1$", -0.0200, -0.0010, -0.0054, 0.0001, format="%.4f")
            with cols[2]: a2 = st.slider("$a_2$", -0.000200, -0.000010, -0.000086, -0.000001, format="%.6f")

            discharge_manufacturer = np.linspace(100,400,100)
            head_pump_manufacturer = a0 + a1*discharge_manufacturer + a2*discharge_manufacturer**2

            h_pump_fig = go.Figure()

            h_pump_fig.add_traces(
                [
                    go.Scatter(
                        x = discharge,
                        y = system_head,
                        name="System",
                        hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                        visible='legendonly',
                        line=dict(
                            width=3,
                            dash="longdash",
                            color="cornflowerblue")
                    ),
                    go.Scatter(
                        x=discharge_manufacturer,
                        y=head_pump_manufacturer,
                        name="Centrifugal pump",
                        hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                        line=dict(
                            width=8, 
                            color="purple")
                    ),
                    go.Scatter(
                        x = [200,195],
                        y = [0,30],
                        name="Positive displacement",
                        hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                        visible='legendonly',
                        line=dict(
                            width=8,
                            color="chocolate")
                    ),
                ]
            )
            
            h_pump_fig.add_hline(
                y = a0,
                name= "Shutoff head",
                annotation=dict(
                    text="Shutoff head",
                    font_size=19
                ),
                line=dict(
                        width=2,
                        dash="dashdot", 
                        color="#ff0044")
            )

            h_pump_fig.add_vline(
                x = 260,
                name= "Rated capacity",
                annotation=dict(
                    text="Rated capacity",
                    font_size=19,
                    font_color="purple"
                ),
                annotation_position = "top",
                line=dict(
                        width=2,
                        dash="dot", 
                        color="purple")
            )

            h_pump_fig.update_layout(
                height=600,
                margin=dict(t=40),
                #title_text = '''System curve''',
                yaxis=dict(
                    title="Head pump [m]",
                    range=[0,30],
                    **axis_format),
                xaxis=dict(
                    title="Discharge [L/min]",
                    range=[0,500],
                    **axis_format),
                legend=dict(
                    title="Curves",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top", y=0.30,
                    xanchor="left", x=0.05
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(h_pump_fig, use_container_width=True)
        
        with tabs[1]:  ## Efficiency vs Q plot
            efficiency_manufacturer =  (-0.0007*np.power(discharge_manufacturer, 2) + 0.3667*discharge_manufacturer + 15)/100
            
            r"""
            🦾 **Efficiency:** ratio of the power output to the power input 
            """

            efficiency_fig = go.Figure()

            efficiency_fig.add_trace(
                go.Scatter(
                    x=discharge_manufacturer,
                    y=efficiency_manufacturer,
                    name="Centrifugal pump",
                    hovertemplate="<i>η</i> = %{y:.2f} <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=8, 
                        color="purple")
                )
            )

            efficiency_fig.add_vline(
                x = 260,
                name= "Optimal operation point",
                annotation=dict(
                    text="Optimal operation point",
                    font_size=19,
                    font_color="purple"
                ),
                annotation_position="top",
                line=dict(
                        width=2,
                        dash="dot", 
                        color="purple")
            )

            efficiency_fig.update_layout(
                height=600,
                margin=dict(t=40),
                yaxis=dict(
                    title="Efficiency [-]",
                    range=[0,1.0],
                    **axis_format),
                xaxis=dict(
                    title="Discharge [L/min]",
                    range=[0,500],
                    **axis_format),
                legend=dict(
                    title="Curves",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top", y=0.96,
                    xanchor="right", x=0.96
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(efficiency_fig, use_container_width=True) 

        with tabs[2]:  ## Power vs Q plot
            r"""
            🔋 **Power input:** required by the pump.
            $$
                \mathcal{P} = \dfrac{Q H_p \rho g}{\eta}
            $$
            
            🐎 **Brake horsepower:** power input in horsepower units.
            """
            brake_power_manufacturer = discharge_manufacturer/(1000*60) * head_pump_manufacturer * 1000 * 9.71 / efficiency_manufacturer

            power_fig = go.Figure()

            power_fig.add_trace(
                go.Scatter(
                    x=discharge_manufacturer,
                    y=brake_power_manufacturer,
                    name="Centrifugal pump",
                    hovertemplate="<i><b>P</b></i> = %{y:.1f} W <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=8, 
                        color="purple")
                )
            )
            
            power_fig.update_layout(
                height=600,
                margin=dict(t=40),
                #title_text = '''System curve''',
                yaxis=dict(
                    title="Power input [W]",
                    range=[0,2000],
                    **axis_format),
                xaxis=dict(
                    title="Discharge [L/min]",
                    range=[0,500],
                    **axis_format),
                legend=dict(
                    title="Curves",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top", y=0.96,
                    xanchor="right", x=0.96
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(power_fig, use_container_width=True)

        with tabs[3]:  ## NPSH vs Q plot
            r"""
            🫧 **Net Positive Suction Head (NPSHr):** represents the pressure drop between the eye
            of the pump and the tip of the impeller vanes.
            """
            npsh_manufacturer = 2.93 - 0.017*discharge_manufacturer + 0.000037*discharge_manufacturer**2

            npsh_fig = go.Figure()

            npsh_fig.add_trace(
                go.Scatter(
                    x=discharge_manufacturer,
                    y=npsh_manufacturer,
                    name="Centrifugal pump",
                    hovertemplate="<i><b>P</b></i> = %{y:.1f} W <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=8, 
                        color="purple")
                )
            )
            
            npsh_fig.update_layout(
                height=600,
                margin=dict(t=40),
                #title_text = '''System curve''',
                yaxis=dict(
                    title="NPSH [m]",
                    range=[0,3],
                    **axis_format),
                xaxis=dict(
                    title="Discharge [L/min]",
                    range=[0,500],
                    **axis_format),
                legend=dict(
                    title="Curves",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top", y=0.96,
                    xanchor="right", x=0.96
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(npsh_fig, use_container_width=True)

        "****"

        r"## Pump Selection"
        "Check a catalogue!"
        html = r"""
        <div>
            <object data="https://www.centrifugal-pump-online.com/MD.pdf" type="application/pdf" width="100%" height="800">
            </object>
        </div>
        """
        st.components.v1.html(html, height=800, scrolling=True)

    elif option == "Cavitation":
        r"""
        ### 🌘 Water phase diagram
        """ 

        st.image("https://www.101diagrams.com/wp-content/uploads/2017/09/phase-diagram-of-water-image.jpg", use_column_width=True)
        
        r"""
        *****
        ### 🫧 Cavitation

        """
        st.video("https://www.youtube.com/watch?v=0dd6AlyOnfc")
        st.caption("Source: [youtube.com/@MntengDenver](https://www.youtube.com/watch?v=0dd6AlyOnfc)")

        r"""
        *****
        ### 🪠 Pressure drop in a pump suction line
        """
        tabs = st.tabs([
            "**⛲ No cavitation**", 
            "**✨ Cavitation in line**", 
            "**🫧 Cavitation in pump**"]
        )
        with tabs[0]: st.pyplot(suction_pipeline_cavitate(where=False))
        with tabs[1]: st.pyplot(suction_pipeline_cavitate(where="pipe"))
        with tabs[2]: st.pyplot(suction_pipeline_cavitate(where="pump"))

        r"""

        Energy balance between the suction tank and the eye of the pump:
        $$
            z_{\rm tank} + \dfrac{p_{\rm tank}}{\gamma} = z_{\rm eye} + \dfrac{p_{\rm eye,abs}}{\gamma} + \dfrac{V^2}{2g} + h_L
        $$

        $$
            \dfrac{p_{\rm eye,abs}}{\gamma} = \underbrace{z_{\rm tank} - z_{\rm eye}}_{\substack{\textsf{Difference in} \\ \textsf{elevation} \\ \Delta z}} + \dfrac{p_{\rm tank,abs}}{\gamma} - \dfrac{V^2}{2g} - h_L
        $$

        $$
            \dfrac{p_{\rm eye,abs}}{\gamma} = \Delta z + \dfrac{p_{\rm atm}}{\gamma} - \dfrac{V^2}{2g} - h_L
        $$

        To avoid fluid cavitation, the pressure cannot be lower than its vapor pressure:
        
        $$
            \dfrac{p_{\rm eye,abs}}{\gamma} >  \dfrac{p_{\rm vapor}}{\gamma}
        $$
        
        ### ⚬ Net Pressure Suction Head -- $\mathtt{NPSH}$
        
        The pressure head drops even further inside a centrifugal pump. 
        Pump manufacturers often especify the minimum required pressure at the 
        eye $(\mathtt{NPSH_r})$.

        """ 
        cols = st.columns(2)

        with cols[0]:
            r"""
            #### $\mathtt{NPSH_a}$

            Absolute head  at the suction eye of the pump

            $$
                \mathtt{NPSH_a} = \dfrac{p_{\rm eye,abs}}{\gamma} +  \dfrac{V^2}{2g} - \dfrac{p_{\rm vapor}}{\gamma}
            $$
            """

        with cols[1]:
            r"""
            #### $\mathtt{NPSH_r}$

            Minimum pressure required at the suction eye to keep the pump from cavitating 
            
            $$
                \mathtt{NPSH_r} = \substack{\textsf{Check pump} \\ \textsf{characteristic curve!}}
            $$
            
            """

        r"""
        $$
            \textsf{To avoid cavitation:} \quad \mathtt{NPSH_a} > \mathtt{NPSH_r}
        $$
        """

        r"""
        *****
        ### Euler number

        $$
            \mathsf{E_u} = \dfrac{\textsf{Pressure forces}}{\textsf{Inertial forces}} = \dfrac{p_\textsf{U} - p_\textsf{D}}{\rho u^2}
        $$

        | Parameter | Symbol   | Units  |
        |:---------|:--------:|:------------------:|
        |Pressure upstream   | $p_\textsf{U}$   | Force/Area        | 
        |Pressure downstream   | $p_\textsf{D}$   | Force/Area        | 
        |Characteristic velocity | $u$    | Length/Time  |
        |Fluid density | $\rho$    | Mass/Volume  | 

        &nbsp;

        In an ideal flow with no energy losses, $\mathsf{E_u} = 0$

        ### Cavitation number 

        $$
            \sigma = \dfrac{\mathtt{NPSH_r}}{H_p}
        $$
        """

    elif option == "Pumps in series/parallel":
        r" ### 🚧 Under construction 🚧"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

#############################################

def swamme_jain(relative_roughness:float, reynolds_number:float):
    fcalc = 0.25 / np.power(np.log10(relative_roughness/3.7 + 5.74/np.power(reynolds_number, 0.9)), 2)
    return fcalc

swamme_jain = np.vectorize(swamme_jain)

@st.cache_data
def get_roughness_database():
    with open("assets/pipe_roughness.json") as f:
        pipe_roughness_db = json.load(f)
    return pipe_roughness_db

def tank(ax, p:Point, width:float, height:float):
    ax.add_patch(Rectangle(p, width, height, fc="#0000aa10", zorder=0))
    ax.plot(
        [p.x, p.x, p.x + width, p.x + width],
        [p.y + 1.1*height, p.y, p.y, p.y + 1.1*height],
        lw=2, c="k", zorder=1)

def pump(ax, p:Point, radius:float):
    ax.add_patch(Circle(p, radius, fc="#11eeee", ec="#44444450", zorder=2))
    ax.text(p.x, p.y, r"$\mathtt{P}$", ha='center', va='center')

def get_realistic_pump():
    import requests
    from PIL import Image
    from io import BytesIO
    
    url = "https://www.pump.co.uk/images/cm50-range-of-end-suction-centrifugal-pumps-p5471-2913_medium.jpg"
    r = requests.get(url, stream=True)

    img = Image.open(BytesIO(r.content), formats=["png", "jpg"])

    return img

def realistic_pump(ax, p:Point, size:float):
    
    if "realistic_pump" not in st.session_state:
        img = get_realistic_pump()
        st.session_state.realistic_pump = img
    else:
        img = st.session_state.realistic_pump
        
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox

    imagebox = OffsetImage(img, zoom=size, cmap="bone_r")

    ax.add_artist(
        AnnotationBbox(
            imagebox, 
            p,
            frameon=False,
            zorder=1
        )
    )

def suction_pipeline_cavitate(where:str) -> plt.figure:

    fig, ax = plt.subplots()

    if where == "pipe":
        tank_xy = Point(-1, -3.8)

    elif where == "pump":
        tank_xy = Point(-1, -2.2)

    else:
        tank_xy = Point(-1, 0)

    tank(ax, tank_xy, 3, 2) 
    realistic_pump(ax, Point(10.6, 0.2), 0.10)
    
    ## Pipeline    
    ax.plot([2.1, 3.0, 8.5, 10.0, 10.0],  [tank_xy.y+0.2, tank_xy.y+0.2, 0.1, 0.1, 10.0], lw=7, color='gray', alpha=0.7, zorder=1)

    ## HGL
    #ax.plot([2.1, 9.0, 10., 10.5], [2.0, -0.5, -1.5, 6.0], lw=1.5, c='k', ls=":", label="HGL")

    ax.plot([2.1, 9.6, 10, 10.5], [tank_xy.y+2.0, tank_xy.y-0.5, tank_xy.y-1.5, 6.0], lw=1.5, c='k', ls=":", label="HGL")

    # Datum
    ax.axhline(-5.5, xmin=0.5, lw=1, color='k', ls="dashed", zorder=0)
    ax.text(6, -5.3, r"Datum: Vaccum", ha="left", fontdict=dict(size=8))

    # Atmospheric pressure    
    ax.axhline(tank_xy.y+2.0, lw=1, color='gray', ls=":")
    ax.text(-2, tank_xy.y+2.2, r"$P_{\rm atm}/\gamma$", ha="center", fontdict=dict(size=8))

    # Vapor pressure    
    ax.axhline(-4, lw=1, color='gray', ls=":")
    ax.text(-2, -3.8, r"$P_{\rm vapor}/\gamma$", ha="center", fontdict=dict(size=8))

    # Vapor pressure    
    ax.axhline(-3, lw=1, color='gray', ls=":")
    ax.text(-2, -2.8, r"$\mathtt{NPSHr}$", ha="center", fontdict=dict(size=8))

    # Final touches
    ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_xlim(-2.5, 13.5)
    ax.set_ylim(-6, 6.0)
    ax.set_aspect('equal')
    #ax.grid(True)
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig

def pump_and_pipeline():
    
    fig, ax = plt.subplots()
    
    # Tank A
    tank(ax, Point(0,0), 2, 1.1)
    ax.plot([-0.8, 3], [1.1, 1.1], lw=1, c='gray', ls=":")
    ax.plot([-0.5, -0.5], [-1, 1.1], marker="x", lw=1, c='gray', ls=":")
    ax.text(-0.6, 0, r"$H_A$", ha="right", va="center", fontdict=dict(color='gray', size=12))

    # Tank B
    tank(ax, Point(7.5,3.5), 2, 1.1)
    ax.plot([2.0, 11], [4.6, 4.6], lw=1, c='gray', ls=":")
    ax.plot([10.4, 10.4], [-1, 4.6], marker="x", lw=1, c='gray', ls=":")
    ax.text(10.5, 2, r"$H_B$", ha="left", va="center", fontdict=dict(color='gray', size=12))

    # Energy difference
    ax.plot([2.5, 2.5], [1.1, 4.6], marker="x", lw=2, c='darkorange', ls=":")
    ax.text(2.4, 3, r"$H_{\mathsf{SH}}$", ha="right", va="center", fontdict=dict(color='darkorange', size=12))

    # Head losses
    ax.plot([2.5, 2.5], [4.6, 5.6], marker="x", lw=2, c='purple', ls=":")
    ax.text(2.4, 5.1, r"$h_L$", ha="right", va="center", fontdict=dict(color='purple', size=12))
    
    # HGL
    ax.plot([2.5, 7.5], [5.6, 4.6], lw=2, c='k', ls=":", label="HGL")

    # Draw the pipe
    ax.plot([2.1, 3.0, 6.5, 7.45],  [0.1, 0.1, 4, 4], lw=4, color='gray', alpha=0.7, zorder=0)
    
    # Draw the pump
    pump(ax, Point(2.5, 0.1), 0.3)
    
    # Datum
    ax.axhline(-1, lw=1, color='k', ls="dashed")
    ax.text(1, -0.8, r"Datum", ha="center", fontdict=dict(size=6))
    
    # Final touches
    ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.85, 0.2))
    ax.set_xlim(-1.5, 11.5)
    ax.set_ylim(-1.2, 6.0)
    ax.set_aspect('equal')
    #ax.grid(True)
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig

if __name__ == "__main__":
    main()