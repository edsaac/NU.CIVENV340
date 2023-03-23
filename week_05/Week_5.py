import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt


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
        st.image("https://upload.wikimedia.org/wikipedia/commons/9/92/Japan_Kyoto_philosophers_walk_DSC00297.jpg", use_column_width=True)
        st.caption("Lake Biwa Canal. Source: [wikimedia.org](https://upload.wikimedia.org/wikipedia/commons/9/92/Japan_Kyoto_philosophers_walk_DSC00297.jpg)")
        
        r"""
        ### Open-channel flow classification
        """
        r"### 🚧 Under construction"
    
    elif option == "Section geometry":
        r"""
        ## 📜 Some definitions

        |Parameter | Symbol | Description | Units |
        |:---------|:------:|:------------|:-----:|
        |Discharge |$Q$     |Volumetric flow rate| Volume/Time |
        |Flow area |$A$     |Cross-sectional area of the flow| Area |
        |Average velocity| $V$ | $Q = VA$ | Length/Time |
        |Depth     |$y$     |Vertical distance from the channel bottom to the free surface| Length |
        |Top width |$T$     |Width at the surface | Length |
        |Bottom width | $b$ | Width at the bottom | Length |
        |Wetted perimeter | $P_w$| Contact length of water and the channel | Lenght |
        |Hydraulic depth  | $D_h$| $D_h = \dfrac{A}{T}$| Lenght |
        |Hydraulic radius | $R_h$| $R_h = \dfrac{A}{P_w}$ | Lenght |
        |Bottom slope     | $S_0$| Longitudinal slope | - |
        |Side slope       | $m$  | 1 vertical over $m$ horizontal | - |
        """
        st.caption("Adapted from pp. 198-199 - Course textbook")

        r"""
        *****
        ## 📐 Cross-section geometry
        """
        tabs = st.tabs(["Rectangular", "Trapezoidal", "Triangular", "Circular"])

        with tabs[0]: #Rectangular
            cols = st.columns(2)
            with cols[0]:
                st.pyplot(draw_sections("rectangle"))
            
            with cols[1]: #Equations
                r"""
                $$
                    \begin{align*}
                        A &= by \\
                        \\
                        P_w &= b + 2y \\
                        \\
                        R_h &= \dfrac{by}{b + 2y}\\
                        \\
                        T &= b \\
                        \\
                        D_h &= y
                    \end{align*}
                $$
                """

        with tabs[1]: #Trapezoidal
            cols = st.columns(2)
            with cols[0]:
                st.pyplot(draw_sections("trapezoid"))

            with cols[1]:
                r"""
                $$
                    \begin{align*}
                        A &= (b+my)y \\
                        \\  
                        P_w &= b + 2y\sqrt{1+m^2} \\
                        \\
                        R_h &= \dfrac{(b+my)y}{b + 2y\sqrt{1+m^2}}\\
                        \\
                        T &= b + 2my \\
                        \\
                        D_h &= \dfrac{(b+my)y}{b + 2my}
                    \end{align*}
                $$
                """

        with tabs[2]: #Triangular
            cols = st.columns(2)

            with cols[0]:
                st.pyplot(draw_sections("triangle"))

            with cols[1]:
                r"""
                $$
                    \begin{align*}
                        A &= my^2 \\
                        \\
                        P_w &= 2y\sqrt{1+m^2} \\
                        \\
                        R_h &= \dfrac{my}{2\sqrt{1+m^2}}\\
                        \\
                        T &= 2my \\
                        \\
                        D_h &= \dfrac{y}{2}
                    \end{align*}
                $$
                """

        with tabs[3]: #Circular
            cols = st.columns(2)
            
            with cols[0]:
                st.pyplot(draw_sections("circle"))

            with cols[1]:
                r"""
                $$
                    \begin{align*}
                        \theta &= \pi - \arccos{\left( \dfrac{y - d_0/2}{d_0/2} \right)} \\
                        \\
                        A &= \tfrac{1}{8}\left( 2\theta - \sin{2\theta} \right)d_0^2 \\
                        \\
                        P_w &= \theta d_0 \\
                        \\
                        R_h &= \dfrac{d_0}{4} \left( 1 - \dfrac{\sin{2\theta}}{2\theta} \right) \\
                        \\
                        T &= d_0 \sin{\theta} = 2\sqrt{y(d_0 - y)} \\
                        \\
                        D_h &= \dfrac{d_0}{8}\left( \dfrac{2\theta - \sin{2\theta}}{\sin{\theta}} \right)
                    \end{align*}
                $$
                """
            
    elif option == "Specific energy":
        r"### 🚧 Under construction"

    elif option == "Froude number":
        r"### 🚧 Under construction"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def draw_sections(shape:str):
    from matplotlib.patches import Rectangle, Polygon, Circle
    
    p = Point(0,0)
    width = 2.0
    height = 1.0

    fig, ax = plt.subplots()

    if shape == "rectangle":
        
        ax.add_patch(
            Rectangle(p, width, height, 
                hatch="/////", ec="#0000ff40",
                fc="#0000ff10", zorder=0)
        )
        
        ax.plot(
            [p.x, p.x, p.x + width, p.x + width],
            [p.y + 1.1*height, p.y, p.y, p.y + 1.1*height],
            lw=2, c="k", zorder=2)

        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(p.x - 0.15, 0.5 * height, r"$y$", fontdict=dict(size=20, color='gray'),ha='right')

        # Width
        ax.plot([p.x, p.x + width], [p.y - 0.1, p.y - 0.1], marker="o", c="gray")
        ax.text(p.x + 0.5 * width, p.y - 0.15, r"$b = T$", fontdict=dict(size=20, color='gray'), ha='center', va='top')

    if shape == "trapezoid":
        ax.add_patch(
            Polygon([(p.x, p.y + height), (p.x + 0.5, p.y), (p.x + 1.5, p.y), (2, p.y + height)], 
                hatch="/////", ec="#0000ff40",
                fc="#0000ff10", zorder=0, closed=True))
        ax.plot(
            [-0.1, 0.5, 1.5, 2.1], 
            [1.2, 0, 0, 1.2],
            lw=2, c="k", zorder=2
        )
        
        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(p.x - 0.15, 0.5 * height, r"$y$", fontdict=dict(size=20, color='gray'),ha='right')

        # Top width
        ax.plot([p.x, p.x + width], [p.y + height + 0.1 , p.y + height + 0.1], marker="o", c="gray")
        ax.text(p.x + 0.5 * width, p.y + height + 0.15, r"$T$", fontdict=dict(size=20, color='gray'), ha='center', va='bottom')
        
        # Bottom width
        ax.plot([p.x + 0.5, p.x + width - 0.5], [p.y - 0.1 , p.y - 0.1], marker="o", c="gray")
        ax.text(p.x + 0.5 * width, p.y - 0.15, r"$b$", fontdict=dict(size=20, color='gray'), ha='center', va='top')
        
        # Slope
        ax.plot([1.70, 1.85, 1.85], [0.3, 0.3, 0.6], marker=".", c="gray")
        ax.text(1.77, 0.29, r"$m$", fontdict=dict(size=20, color='gray'), ha='center', va='top')
        ax.text(1.85, 0.45, r"$1$", fontdict=dict(size=20, color='gray'), ha='left', va='center')

    if shape == "triangle":
        ax.add_patch(
            Polygon([(p.x, p.y + height), (p.x + 0.5*width, p.y), (p.x + width, p.y + height)], 
                hatch="/////", ec="#0000ff40",
                fc="#0000ff10", zorder=0, closed=True))
        
        ax.plot(
            [p.x - 0.1 , p.x + 0.5*width, p.x + width + 0.1], 
            [p.y + height + 0.1, p.y, p.y + height + 0.1],
            lw=2, c="k", zorder=2
        )
        
        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(p.x - 0.15, 0.5 * height, r"$y$", fontdict=dict(size=20, color='gray'),ha='right')

        # Top width
        ax.plot([p.x, p.x + width], [p.y + height + 0.1 , p.y + height + 0.1], marker="o", c="gray")
        ax.text(p.x + 0.5 * width, p.y + height + 0.15, r"$T$", fontdict=dict(size=20, color='gray'), ha='center', va='bottom')
        
        # Slope
        ax.plot([1.35, 1.65, 1.65], [0.3, 0.3, 0.6], marker=".", c="gray")
        ax.text(1.50, 0.29, r"$m$", fontdict=dict(size=20, color='gray'), ha='center', va='top')
        ax.text(1.67, 0.45, r"$1$", fontdict=dict(size=20, color='gray'), ha='left', va='center')

    if shape == "circle":
        from matplotlib.patches import Arc

        c = Point(1.1,0.9)
        r = 0.85
        ax.add_patch(
            Circle(c, r, 
                fc="#0000ff00", zorder=0,
                ec="k", lw=2))

        ax. add_patch(
            Arc(c, 2*r, 2*r, 
                theta1=150, theta2=30, 
                hatch="/////", ec="#0000ff40", zorder=0)
        )
        
        # Center
        ax.plot([c.x], [c.y], lw=0, marker='o', c='k')
        
        # Diameter
        ax.plot([p.x-0.2, p.x-0.2], [c.y - r, c.y + r], marker="o", c="gray")
        ax.text(p.x - 0.21, c.y, r"$d_0$", fontdict=dict(size=20, color='gray'),ha='right')

        # Depth
        ax.plot([p.x+0.1, p.x+0.1], [c.y - r, c.y + 0.42], marker="o", c="gray")
        ax.text(p.x + 0.08, c.y - 0.22, r"$y$", fontdict=dict(size=20, color='gray'),ha='right')

        # Top width
        ax.plot([0.38, 1.82], [1.31 , 1.31], marker="o", c="gray")
        ax.text(0.5*(1.82+0.38), 1.32 ,r"$T$", fontdict=dict(size=20, color='gray'), ha='center', va='bottom')

        # Angle
        ax.plot([c.x, c.x, c.x + r], [c.y - r - 0.1, c.y, c.y + r - 0.36], ls="dotted", c="gray")
        ax.text(1.35, 0.75, r"$\theta$", fontdict=dict(size=20, color='gray'), ha='left', va='center')
        
        ax. add_patch(
            Arc(c, 0.5*r, 0.5*r, 
                theta1=270, theta2=30, 
                ec="gray", lw=2, zorder=1)
        )

    # Final touches
    #ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_xlim(-0.5, 2.2)
    ax.set_ylim(-0.5, 2)
    ax.set_aspect('equal')
    #ax.grid(True)
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig
    
if __name__ == "__main__":
    main()