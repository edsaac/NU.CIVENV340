import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pickle
import numpy as np
import json

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

            fig = go.Figure([
                go.Scatter(
                    x = discharge,
                    y = head_pump,
                    name="System curve",
                    hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} m³/s</b>",
                    line=dict(
                        width=5, 
                        color="#018749")
                )
            ])
            
            fig.add_hline(
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
            

            fig.update_layout(
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
            
            st.plotly_chart(fig, use_container_width=True)
    
        "****"

    elif option == "Types of pumps":
        r" ### 🚧 Under construction 🚧"

    elif option == "Characteristic curves":
        r" ### 🚧 Under construction 🚧"

    elif option == "Cavitation":
        r" ### 🚧 Under construction 🚧"

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

def pump_and_pipeline():

    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])

    from matplotlib.patches import Rectangle, Circle
    
    def tank(ax, p:Point, width:float, height:float):
        ax.add_patch(Rectangle(p, width, height, fc="#0000aa10", zorder=0))
        ax.plot(
            [p.x, p.x, p.x + width, p.x + width],
            [p.y + 1.1*height, p.y, p.y, p.y + 1.1*height],
            lw=2, c="k", zorder=1)

    def pump(ax, p:Point, radius:float):
        ax.add_patch(Circle(p, radius, fc="#11eeee", ec="#44444450", zorder=2))
        ax.text(p.x, p.y, r"$\mathtt{P}$", ha='center', va='center')
    
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