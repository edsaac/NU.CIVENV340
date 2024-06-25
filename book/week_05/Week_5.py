import streamlit as st
import numpy as np
import plotly.graph_objects as go

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

from typing import Literal
from collections import namedtuple

from book.common import axis_format
from .subpages import find_critical_depth

Point = namedtuple("Point", ["x", "y"])

TOC = Literal[
    "Open channel flow",
    "Section geometry",
    "Specific energy",
    "Froude number",
    "~Critical depth calculation",
]


def page_week_05(option: TOC):
    st.title(option.replace("~", ""))

    if option == "Open channel flow":
        url = "https://upload.wikimedia.org/wikipedia/commons/9/92/Japan_Kyoto_philosophers_walk_DSC00297.jpg"
        st.image(url, use_column_width=True)
        st.caption(f"Lake Biwa Canal. Source: [wikimedia.org]({url})")

        st.subheader("Open-channel flow classification")

        tabs = st.tabs(
            [
                "**Uniform**",
                "**Gradually varied** (Accelerating)",
                "**Gradually varied** (Slowing down)",
                "**Rapidly varied**",
            ]
        )

        with tabs[0]:  ## Uniform flow
            st.pyplot(draw_profiles(which="uniform"))

            cols = st.columns(3)
            with cols[0]:
                st.latex(R"y_1 = y_2")

            with cols[1]:
                st.latex(R"\dfrac{V^2_1}{2g} = \dfrac{V^2_2}{2g}")

            with cols[2]:
                st.latex("S_0 = S_w = S_e")

        with tabs[1]:  ## GVF -> Accelerates
            st.pyplot(draw_profiles(which="gvf_accelerate"))

            cols = st.columns(3)
            with cols[0]:
                st.latex("y_1 > y_2")

            with cols[1]:
                st.latex(R"\dfrac{V^2_1}{2g} < \dfrac{V^2_2}{2g}")

            with cols[2]:
                st.latex(R"S_0 \neq S_w \neq S_e")

        with tabs[2]:  ## GVF -> Deaccelerates
            st.pyplot(draw_profiles(which="gvf_slowing"))

            cols = st.columns(3)
            with cols[0]:
                st.latex(R"y_1 < y_2")

            with cols[1]:
                st.latex(R"\dfrac{V^2_1}{2g} > \dfrac{V^2_2}{2g}")

            with cols[2]:
                st.latex(R"S_0 \neq S_w \neq S_e")

        with tabs[3]:  ## RVF
            url = "https://www.youtube.com/watch?v=nX6aemsdFIo"
            st.video(url, muted=True)
            st.caption(f"Source: [youtube.com/@fluidsin4k719]({url})")

    elif option == "Section geometry":
        st.markdown(
            R"""
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
        )

        st.caption(
            "Adapted from *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed., pp. 198-199"
        )

        st.markdown(
            R"""
            *****
            ## 📐 Cross-section geometry
            """
        )

        tabs = st.tabs(["Rectangular", "Trapezoidal", "Triangular", "Circular"])

        with tabs[0]:  # Rectangular
            cols = st.columns(2)
            with cols[0]:
                st.pyplot(draw_sections("rectangle"))

            with cols[1]:  # Equations
                st.latex(
                    R"""
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
                    """
                )

        with tabs[1]:  # Trapezoidal
            cols = st.columns(2)
            with cols[0]:
                st.pyplot(draw_sections("trapezoid"))

            with cols[1]:
                st.latex(
                    R"""
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
                    """
                )

        with tabs[2]:  # Triangular
            cols = st.columns(2)

            with cols[0]:
                st.pyplot(draw_sections("triangle"))

            with cols[1]:
                st.latex(
                    R"""
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
                    """
                )

        with tabs[3]:  # Circular
            cols = st.columns(2)

            with cols[0]:
                st.pyplot(draw_sections("circle"))

            with cols[1]:
                st.latex(
                    R"""
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
                    """
                )

    elif option == "Specific energy":

        st.subheader("Total and specific energy", anchor=False)

        st.markdown(
            R"""
            The **total energy** per unit weight of water flowing in an open channel is the sum of:
            - Kinetic energy
            - Pressure energy
            - Potential energy (elevation above a datum line)
            """
        )

        st.latex(R"H = \underbrace{z}_{\substack{ \textsf{Elevation} \\ \textsf{head} }} + \underbrace{ \dfrac{p}{\gamma} }_{ \substack{ \textsf{Pressure} \\ \textsf{head} }} + \underbrace{ \alpha\dfrac{V^2}{2g} }_{ \substack{\textsf{Kinetic} \\ \textsf{head}}}")

        st.markdown(
            R"""
            |Parameter | Symbol | Units |
            |:---------|:------:|:-----:|
            |Total energy per unit weight |$H$ | Length |
            |Pressure head |$p/\gamma$ | Length |
            |Energy coefficient |$\alpha \in [1.0, 1.20] $ | - |
            |Mean velocity |$V$ | Length/Time |

            &nbsp;

            On a plane surface, the water depth $y$ represents the pressure head $p/\gamma$.


            The **specific energy** is the energy head measured with respect of the channel bottom
            """
        )

        st.latex(R"E = y + \dfrac{V^2}{2g} = y + \dfrac{Q^2}{2gA^2}")
         
        st.divider()
        
        st.header("Specific energy curve", anchor=False)

        st.markdown(R"""
            For a given value of $E$, the discharge can go through either a supercritical depth or
            a subcritical depth. This pair of depths are known as **alternate depths**.            
            """
        )

        cols = st.columns([2, 1], vertical_alignment="center")

        with cols[1]:  ## Controls for plot
            width = st.slider("Width -- $b$ [m]", 0.1, 10.0, 3.0, 0.1)
            discharge = st.slider("Discharge -- $Q$ [m³/s]", 1.0, 30.0, 15.0, 0.1)

            depth = np.geomspace(0.01, 10, 100)
            area = width * depth
            specific_energy = depth + np.power(discharge, 2) / (
                2 * 9.81 * np.power(area, 2)
            )

            critical_i = np.argmin(specific_energy)

            all_discharges = np.linspace(0.5, 300, 100)
            critical_state = np.cbrt(np.power(all_discharges, 2) / (9.81 * width**2))
            all_specific_energy = critical_state + np.power(all_discharges, 2) / (
                2 * 9.81 * np.power(width * critical_state, 2)
            )

        with cols[0]:  ## Plotly plot
            fig = go.Figure()
            fig.add_trace(  ## Specific energy
                go.Scatter(
                    x=specific_energy,
                    y=depth,
                    name="Specific energy",
                    hovertemplate="<i><b>E</b></i> = %{x:.1f} m <br>y = %{y:.1f} m",
                    line=dict(width=8, color="purple"),
                )
            )

            fig.add_trace(  ## Critical point
                go.Scatter(
                    x=[specific_energy[critical_i]],
                    y=[depth[critical_i]],
                    name="Critical flow",
                    mode="markers",
                    hovertemplate="<i><b>E<sub>min</sub></b></i> = %{x:.1f} m <br><i>y<sub>c</sub></i> = %{y:.1f} m",
                    marker=dict(
                        size=20,
                        color="#ff8811",
                        opacity=0.7,
                        line=dict(color="MediumPurple", width=2),
                    ),
                )
            )

            fig.add_trace(  ## Critical state
                go.Scatter(
                    x=all_specific_energy,
                    y=critical_state,
                    name="Critical state <br><i>changes in Q</i>",
                    hovertemplate="<i><b>E<sub>min</sub></b></i> = %{x:.1f} m <br><i>y<sub>c</sub></i> = %{y:.1f} m",
                    line=dict(dash="dot", color="orange"),
                )
            )

            fig.add_trace(  ## 45deg line
                go.Scatter(
                    x=[-10, 10],
                    y=[-10, 10],
                    name="<i>E</i> > <i>y<i>",
                    mode="lines",
                    line=dict(width=2, color="pink", dash="dot"),
                )
            )

            fig.add_hrect(  ## Supercritical region
                y0=0.0,
                y1=depth[critical_i],
                annotation_text="Supercritical",
                annotation_position="top right",
                line_width=0,
                fillcolor="orange",
                opacity=0.1,
            )

            fig.add_hrect(  ## Subcritical region
                y1=10,
                y0=depth[critical_i],
                annotation_text="Subcritical",
                annotation_position="bottom right",
                line_width=0,
                fillcolor="blue",
                opacity=0.1,
            )

            fig.update_layout(
                height=600,
                margin=dict(t=40),
                title_text="""Specific energy for a rectangular channel""",
                yaxis=dict(
                    title="Depth &nbsp; <i>y</i> [m]",
                    range=[0, 10],
                    showspikes=True,
                    **axis_format,
                ),
                xaxis=dict(
                    title="Specific energy &nbsp; <i>E</i> [m]",
                    range=[0, 10],
                    showspikes=True,
                    **axis_format,
                ),
                legend=dict(
                    # title="",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top",
                    y=0.96,
                    xanchor="left",
                    x=0.04,
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.header("Critical flow", anchor=False)

        st.markdown(R"""
            Depth at which the specific energy is minimized
            
            $$
                \dfrac{dE}{dy} = \dfrac{d}{dy} \left(y + \dfrac{Q^2}{2gA^2}\right) = 0 
            $$

            $$
                -\dfrac{Q^2}{gA^3}\dfrac{dA}{dy} + 1 = 0
            $$"""
        )

        st.info("Explain why $dA/dy = T$", icon=":material/person_raised_hand:")
        
        st.markdown(R"""
            $$
                1 - \dfrac{Q^2T}{gA^3} = 0
            $$

            Introducing the hydraulic depth $D_h$,

            $$
                1 - \dfrac{Q^2}{g A^2} \dfrac{1}{D_h} = 0 
            $$

            Specific energy is minimal when 
            $$
                \dfrac{Q^2}{g A^2} \dfrac{1}{D_h} = 1
            $$

            Or in terms of velocity
            $$
                \underbrace{\dfrac{V}{\sqrt{g \, D_h}}}_{\substack{\textsf{Froude} \\ \textsf{number} \\ \mathsf{F_r} }} = 1
            $$
            """
        )

    elif option == "Froude number":
        
        st.header("Critical depth $y_c$", anchor=False)
        
        st.markdown(
            R"""
            The depth that minimizes the specific energy, i.e., follows that
            $$
                \dfrac{Q^2}{g} = A^2 \, D_h
            $$

            For a rectangular channel, an explicit equation for the critical depth can be found:
            $$
                y_c = \sqrt[3]{\dfrac{Q^2}{g \, b^2}}
            $$

            For trapezoidal and circular channels, a numerical approximation is necessary.
            """
        )

        st.info("""
            &nbsp; Check the next section on how to use `scipy.optimize.root` to calculate critical depth in any cross section""",
            icon="👈"
        )

        st.divider()

        st.header(R"Froude number $\mathsf{F_r}$", anchor=False)

        cols = st.columns(3, gap="medium")
        with cols[0]:  # Subcritical
            st.markdown(R"""
                #### Subcritical flow

                $$
                    \begin{align*}
                        y > y_c \\ \mathsf{F_r} < 1.0
                    \end{align*}
                $$
                """
            )

        with cols[1]:  # Critical
            st.markdown(R"""
                #### Critical flow

                $$
                    \begin{align*}
                        y = y_c \\ \mathsf{F_r} = 1.0
                    \end{align*}
                $$
                """
            )

        with cols[2]:  # Subcritical
            st.markdown(R"""
                #### Supercritical flow

                $$
                    \begin{align*}
                        y < y_c \\ \mathsf{F_r} > 1.0
                    \end{align*}

                $$
                """
            )

        url = "https://www.youtube.com/watch?v=cRnIsqSTX7Q"
        st.video(url)
        st.caption(f"Source: [youtube.com/@emulenews]({url})")

    
    elif option == "~Critical depth calculation":
        find_critical_depth()
    
    else:
        st.error("You should not be here!")


def draw_profiles(which: str):

    So = -1 / 10.0  # 1 + x*S0
    x0, x1, x2 = 1, 3, 8

    if which == "uniform":
        Sw = So  # 3 + x*Sw
        Se = So  # 4 + x*Se

    elif which == "gvf_accelerate":
        Sw = 1.5 * So
        Se = 1 / 1.5 * So

    if which == "gvf_slowing":
        So = -1 / 10.0
        Sw = 0.8 * So
        Se = 1 / 0.8 * So

    section1 = [-1, 1 + x1 * So, 3 + x1 * Sw, 4 + x1 * Se]
    section2 = [-1, 1 + x2 * So, 3 + x2 * Sw, 4 + x2 * Se]

    fig, ax = plt.subplots()

    ## Channel bottom
    ax.axline((0, 1), slope=So, lw=2, c="#00000040")
    ax.text(
        x0,
        1 + x0 * So,
        r"Channel bottom",
        ha="center",
        rotation=-7,
        fontdict=dict(size=8, color="0.2"),
    )
    ax.add_patch(
        Polygon(
            [(0, 0.8), (0, 1), (10, 0), (10, -0.2)],
            closed=False,
            hatch="////",
            ec="#00000030",
            fc="#ffffff",
        )
    )

    ## Water surface
    ax.axline((0, 3), slope=Sw, c="navy")
    ax.text(
        x0,
        3 + x0 * Sw,
        r"HGL",
        ha="center",
        rotation=-8,
        fontdict=dict(size=10, color="navy"),
    )

    # ax.add_patch(
    #     Polygon([(0,1), (0,p1.y+1), (10, p2.y), (10,0)],
    #     closed=False, hatch="....", ec="#0000ff10",
    #             fc="#0000ff10", zorder=0)
    # )

    ## EGL
    ax.axline((0, 4), slope=Se, c="mediumseagreen", ls="dashed")
    ax.text(
        x0,
        4 + x0 * Se,
        r"EGL",
        ha="center",
        rotation=-8,
        fontdict=dict(size=10, color="mediumseagreen"),
    )

    # Datum
    ax.axhline(-1, lw=1, color="k", ls="dashed", zorder=0)
    ax.text(1.0, -0.9, r"Datum", ha="center", fontdict=dict(size=8))

    ## Upstream section

    ### Head components - Section 1
    for i, (x, sect) in enumerate(zip([x1, x2], [section1, section2]), start=1):
        ax.plot([x] * 2, [sect[-1], 4.5], ls="dotted", lw=1, c="gray")
        ax.text(
            x, 4.6, f"Section\n{i}", ha="center", fontdict=dict(size=8, color="gray")
        )
        ax.plot([x] * 4, sect, marker="o", ms=4, lw=2, c="darkslategray", ls=":")
        ax.text(
            x + 0.05,
            np.mean(sect[0:2]),
            rf"$z_{i}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )
        ax.text(
            x + 0.05,
            np.mean(sect[1:3]),
            rf"$y_{i}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )
        ax.text(
            x + 0.05,
            np.mean(sect[2:4]),
            rf"$\dfrac{{V^2_{i}}}{{2g}}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=10),
        )

    ### Slopes
    ax.annotate(
        r"$S_0$",
        (5, 1 + 5 * So),
        (5.5, -0.1),
        size=10,
        color="darkslategray",
        ha="left",
        va="top",
        arrowprops=dict(
            arrowstyle="->",
            color="darkslategray",
            shrinkA=8,
            shrinkB=1,
            patchA=None,
            patchB=None,
            connectionstyle="arc3, rad=-0.3",
        ),
    )

    ax.annotate(
        r" $S_w$",
        (5, 3 + 5 * Sw),
        (5.5, 1.5),
        size=10,
        color="navy",
        arrowprops=dict(
            arrowstyle="->",
            color="navy",
            shrinkA=8,
            shrinkB=1,
            patchA=None,
            patchB=None,
            connectionstyle="arc3, rad=-0.3",
        ),
    )

    ax.annotate(
        r" $S_e$",
        (5, 4 + 5 * Se),
        (5.5, 4),
        size=10,
        color="mediumseagreen",
        arrowprops=dict(
            arrowstyle="->",
            color="mediumseagreen",
            shrinkA=8,
            shrinkB=1,
            patchA=None,
            patchB=None,
            connectionstyle="arc3, rad=0.3",
        ),
    )

    # Final touches
    # ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(-1.5, 5.0)
    ax.set_aspect("equal")
    # ax.grid(True, color="lightgray")
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig


def draw_sections(shape: str):
    p = Point(0, 0)
    width = 2.0
    height = 1.0

    fig, ax = plt.subplots()

    if shape == "rectangle":
        ax.add_patch(
            Rectangle(
                p,
                width,
                height,
                hatch="/////",
                ec="#0000ff40",
                fc="#0000ff10",
                zorder=0,
            )
        )

        ax.plot(
            [p.x, p.x, p.x + width, p.x + width],
            [p.y + 1.1 * height, p.y, p.y, p.y + 1.1 * height],
            lw=2,
            c="k",
            zorder=2,
        )

        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(
            p.x - 0.15,
            0.5 * height,
            r"$y$",
            fontdict=dict(size=20, color="gray"),
            ha="right",
        )

        # Width
        ax.plot([p.x, p.x + width], [p.y - 0.1, p.y - 0.1], marker="o", c="gray")
        ax.text(
            p.x + 0.5 * width,
            p.y - 0.15,
            r"$b = T$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="top",
        )

    if shape == "trapezoid":
        ax.add_patch(
            Polygon(
                [
                    (p.x, p.y + height),
                    (p.x + 0.5, p.y),
                    (p.x + 1.5, p.y),
                    (2, p.y + height),
                ],
                hatch="/////",
                ec="#0000ff40",
                fc="#0000ff10",
                zorder=0,
                closed=True,
            )
        )
        ax.plot([-0.1, 0.5, 1.5, 2.1], [1.2, 0, 0, 1.2], lw=2, c="k", zorder=2)

        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(
            p.x - 0.15,
            0.5 * height,
            r"$y$",
            fontdict=dict(size=20, color="gray"),
            ha="right",
        )

        # Top width
        ax.plot(
            [p.x, p.x + width],
            [p.y + height + 0.1, p.y + height + 0.1],
            marker="o",
            c="gray",
        )
        ax.text(
            p.x + 0.5 * width,
            p.y + height + 0.15,
            r"$T$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="bottom",
        )

        # Bottom width
        ax.plot(
            [p.x + 0.5, p.x + width - 0.5], [p.y - 0.1, p.y - 0.1], marker="o", c="gray"
        )
        ax.text(
            p.x + 0.5 * width,
            p.y - 0.15,
            r"$b$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="top",
        )

        # Slope
        ax.plot([1.70, 1.85, 1.85], [0.3, 0.3, 0.6], marker=".", c="gray")
        ax.text(
            1.77,
            0.29,
            r"$m$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="top",
        )
        ax.text(
            1.85,
            0.45,
            r"$1$",
            fontdict=dict(size=20, color="gray"),
            ha="left",
            va="center",
        )

    if shape == "triangle":
        ax.add_patch(
            Polygon(
                [
                    (p.x, p.y + height),
                    (p.x + 0.5 * width, p.y),
                    (p.x + width, p.y + height),
                ],
                hatch="/////",
                ec="#0000ff40",
                fc="#0000ff10",
                zorder=0,
                closed=True,
            )
        )

        ax.plot(
            [p.x - 0.1, p.x + 0.5 * width, p.x + width + 0.1],
            [p.y + height + 0.1, p.y, p.y + height + 0.1],
            lw=2,
            c="k",
            zorder=2,
        )

        # Height
        ax.plot([p.x - 0.1, p.x - 0.1], [p.y, p.y + height], marker="o", c="gray")
        ax.text(
            p.x - 0.15,
            0.5 * height,
            r"$y$",
            fontdict=dict(size=20, color="gray"),
            ha="right",
        )

        # Top width
        ax.plot(
            [p.x, p.x + width],
            [p.y + height + 0.1, p.y + height + 0.1],
            marker="o",
            c="gray",
        )
        ax.text(
            p.x + 0.5 * width,
            p.y + height + 0.15,
            r"$T$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="bottom",
        )

        # Slope
        ax.plot([1.35, 1.65, 1.65], [0.3, 0.3, 0.6], marker=".", c="gray")
        ax.text(
            1.50,
            0.29,
            r"$m$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="top",
        )
        ax.text(
            1.67,
            0.45,
            r"$1$",
            fontdict=dict(size=20, color="gray"),
            ha="left",
            va="center",
        )

    if shape == "circle":
        from matplotlib.patches import Arc

        c = Point(1.1, 0.9)
        r = 0.85
        ax.add_patch(Circle(c, r, fc="#0000ff00", zorder=0, ec="k", lw=2))

        ax.add_patch(
            Arc(
                c,
                2 * r,
                2 * r,
                theta1=150,
                theta2=30,
                hatch="/////",
                ec="#0000ff40",
                zorder=0,
            )
        )

        # Center
        ax.plot([c.x], [c.y], lw=0, marker="o", c="k")

        # Diameter
        ax.plot([p.x - 0.2, p.x - 0.2], [c.y - r, c.y + r], marker="o", c="gray")
        ax.text(
            p.x - 0.21, c.y, r"$d_0$", fontdict=dict(size=20, color="gray"), ha="right"
        )

        # Depth
        ax.plot([p.x + 0.1, p.x + 0.1], [c.y - r, c.y + 0.42], marker="o", c="gray")
        ax.text(
            p.x + 0.08,
            c.y - 0.22,
            r"$y$",
            fontdict=dict(size=20, color="gray"),
            ha="right",
        )

        # Top width
        ax.plot([0.38, 1.82], [1.31, 1.31], marker="o", c="gray")
        ax.text(
            0.5 * (1.82 + 0.38),
            1.32,
            r"$T$",
            fontdict=dict(size=20, color="gray"),
            ha="center",
            va="bottom",
        )

        # Angle
        ax.plot(
            [c.x, c.x, c.x + r],
            [c.y - r - 0.1, c.y, c.y + r - 0.36],
            ls="dotted",
            c="gray",
        )
        ax.text(
            1.35,
            0.75,
            r"$\theta$",
            fontdict=dict(size=20, color="gray"),
            ha="left",
            va="center",
        )

        ax.add_patch(
            Arc(c, 0.5 * r, 0.5 * r, theta1=270, theta2=30, ec="gray", lw=2, zorder=1)
        )

    # Final touches
    # ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_xlim(-0.5, 2.2)
    ax.set_ylim(-0.5, 2)
    ax.set_aspect("equal")
    # ax.grid(True)
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig


if __name__ == "__page__":
    page_week_05()
