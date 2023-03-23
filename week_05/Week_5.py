import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd

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
        <lottie-player src="https://assets9.lottiefiles.com/packages/lf20_cmzv38mj.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "Operation point",
                "Open channel flow",
                "Section geometry",
                "Specific energy",
                "Froude number"
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
    if option == "Operation point":
        r"### Operation point"
        
        cols = st.columns(2)
        
        with cols[0]:
            
            with st.expander("⚙️ **Pump head**"): 
                r"""
                $$
                    H_\textsf{Pump}(Q) = \substack{\textsf{Check pump catalogue} \\ \textsf{for characteristic curve!}}
                $$
                """
        
                discharge_manufacturer = np.arange(100,400,10)
                head_pump_manufacturer = 25.0 - 0.0054*discharge_manufacturer - 0.000086*discharge_manufacturer**2
                pump_df = pd.DataFrame({
                    "Discharge (LPS)" : discharge_manufacturer,
                    "Head (m)" : head_pump_manufacturer})
            
        with cols[1]:
            
            with st.expander("🚿 **System head**"):
                r"""
                #### 

                $$
                    H_\textsf{System}(Q) = H_\textsf{Static head} + KQ^m
                $$
                """
                
                discharge = np.arange(0,500,10)
                static_head = st.slider(r"$H_\textsf{Static head}$", 0.0, 22.0, 10.0, step=0.2)
                head_loss_K = st.slider(r"$K$", 0.1e-4,10e-4,1e-4, 1e-5, key="head_loss", format="%.2e")
                system_head = head_loss_K * discharge**2 + static_head

                system_df = pd.DataFrame({
                    "Discharge (LPS)" : discharge,
                    "Head (m)" : system_head
                })

        all_df = pd.merge(pump_df, system_df, on="Discharge (LPS)", how="outer", suffixes=["_Pump", "_System"]).sort_values(by="Discharge (LPS)")
        all_df["ΔH"] = np.abs(all_df["Head (m)_Pump"] - all_df["Head (m)_System"])

        operation_point = all_df[all_df["ΔH"] == all_df["ΔH"].min()]

        fig = go.Figure()

        fig.add_traces(
            [
                go.Scatter(
                    x = discharge,
                    y = system_head,
                    name="System",
                    hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=4,
                        color="cornflowerblue")
                ),
                go.Scatter(
                    x=discharge_manufacturer,
                    y=head_pump_manufacturer,
                    name="Pump",
                    hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                    line=dict(
                        width=8, 
                        color="purple")
                ),
                go.Scatter(
                    x = operation_point["Discharge (LPS)"],
                    y = operation_point["Head (m)_Pump"],
                    name = "Operation <br>point",
                    mode = "markers",
                    hovertemplate="<i>H<sub>p</sub></i> = %{y:.1f} m <br><b>Q = %{x:.2f} L/min</b>",
                    marker=dict(
                        size=20,
                        color="#ff8811",
                        opacity=0.5,
                        line=dict(
                            color="MediumPurple",
                            width=2
                        )
                    ),
                )
            ]
        )

        fig.update_layout(
            height=600,
            margin=dict(t=40),
            #title_text = '''System curve''',
            yaxis=dict(
                title="Head pump [m]",
                range=[0,30],
                showspikes=True,
                **axis_format),
            xaxis=dict(
                title="Discharge [L/min]",
                range=[0,500],
                showspikes=True,
                **axis_format),
            legend=dict(
                title="Curves",
                font=dict(size=18),
                orientation="v",
                bordercolor="gainsboro",
                borderwidth=1,
                yanchor="top", y=0.30,
                xanchor="right", x=0.95
            ),
            hoverlabel=dict(font_size=18),
        )

        st.plotly_chart(fig, use_container_width=True)

    elif option == "Open channel flow":
        r"### 🚧 Under construction"

    elif option == "Section geometry":
        r"### 🚧 Under construction"

    elif option == "Specific energy":
        r"### 🚧 Under construction"

    elif option == "Froude number":
        r"### 🚧 Under construction"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

if __name__ == "__main__":
    main()