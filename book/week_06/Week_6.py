import streamlit as st

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import plotly.graph_objects as go

import numpy as np

from collections import namedtuple
from urllib.parse import urlparse
from typing import Literal

from .subpages import solve_ivp
from ..common import get_image_as_PIL, axis_format

Side = namedtuple("Side", ["x", "y"])
Point = namedtuple("Point", ["x", "y"])

TOC = Literal[
    "Smooth transitions",
    "Jumps and momentum conservation",
    "Uniform flow",
    "Gradually varied flow",
    "Rivers",
    "Sediments",
    "Lane's diagram",
    "Shear stress",
    "~Solve IVP",
]


def page_week_06(option: TOC):
    
    st.title(option.replace("~", ""))

    if option == "Smooth transitions":
        st.header("🌁 Contractions and expansions", anchor=False)
        st.pyplot(draw_contraction())

        st.markdown(
            R"""
            Assuming that the energy losses through the contraction are negligible,

            $$
                E_1 = E_2
            $$

            Knowing $y_1$ and $Q$, $y_2$ can be predicted given a change in channel
            geometry (i.e., $b_2$ for a rectangular section).

            $$
                y_1 + \dfrac{Q^2}{2gA_1^2} = y_2 + \dfrac{Q^2}{2gA_2^2}
            $$

            The discharge is the same in the two sections, but the cross-sectional area
            will differ as the channel geometry differ. 

            ************
            """
        )

        with st.echo():

            def specific_energy_calc(y, Q, b, units="BG"):
                A = y * b
                g = 32.2 if units == "BG" else 9.81
                return y + np.power(Q, 2) / (2 * g * np.power(A, 2))

        st.divider()

        cols = st.columns([2, 1])
        with cols[1]:  ## Controls for plot
            discharge = st.slider("$Q$ [ft³/s]", 1.0, 100.0, 60.0, 0.1)

            st.markdown("##### Section 1")
            width_1 = st.slider("$b_1$ [ft]", 0.1, 15.0, 12.0, 0.1)
            depth_1 = st.slider("$y_1$ [ft]", 0.1, 5.0, 2.5, 0.1)

            depth = np.geomspace(0.01, 10, 100)
            specific_energy_1 = specific_energy_calc(depth, discharge, width_1)
            ic_1 = np.argmin(specific_energy_1)
            E_1 = specific_energy_calc(depth_1, discharge, width_1)

            st.markdown("##### Section 2")
            width_2 = st.slider("$b_2$ [ft]", 0.1, 15.0, 6.0, 0.1)
            specific_energy_2 = specific_energy_calc(depth, discharge, width_2)
            ic_2 = np.argmin(specific_energy_2)

        with cols[0]:
            fig = go.Figure()

            hovertemplate_eplot = "<i><b>E</b></i> = %{x:.1f} ft <br>y = %{y:.1f} ft"
            fig.add_trace(
                go.Scatter(  ## Section 1
                    x=specific_energy_1,
                    y=depth,
                    name="E<sub>1</sub>(y)",
                    legendgroup="Section1",
                    legendgrouptitle_text="Section 1",
                    hovertemplate=hovertemplate_eplot,
                    line=dict(width=5, color="purple"),
                )
            )

            fig.add_trace(  ## Critical point Section 1
                go.Scatter(
                    x=[specific_energy_1[ic_1]],
                    y=[depth[ic_1]],
                    name="y<sub>c, 1</sub>",
                    legendgroup="Section1",
                    mode="markers",
                    hovertemplate=hovertemplate_eplot,
                    marker=dict(
                        size=20,
                        color="purple",
                        opacity=0.7,
                        line=dict(color="MediumPurple", width=2),
                    ),
                )
            )

            fig.add_vline(
                x=E_1,
                annotation=dict(text="<b>E<sub>1</sub></b>", font_size=20),
                line=dict(dash="dot", width=1),
            )

            fig.add_trace(
                go.Scatter(  ## Section 2
                    x=specific_energy_2,
                    y=depth,
                    name="E<sub>2</sub>(y)",
                    legendgroup="Section2",
                    legendgrouptitle_text="Section 2",
                    hovertemplate="<i><b>E</b></i> = %{x:.1f} m <br>y = %{y:.1f} m",
                    line=dict(width=5, color="green"),
                )
            )

            fig.add_trace(  ## Critical point Section 2
                go.Scatter(
                    x=[specific_energy_2[ic_2]],
                    y=[depth[ic_2]],
                    name="y<sub>c, 2</sub>",
                    legendgroup="Section2",
                    mode="markers",
                    hovertemplate="<i><b>E<sub>min</sub></b></i> = %{x:.1f} m <br><i>y<sub>c</sub></i> = %{y:.1f} m",
                    marker=dict(
                        size=20,
                        color="green",
                        opacity=0.7,
                        line=dict(color="green", width=2),
                    ),
                )
            )

            fig.update_layout(
                height=600,
                margin=dict(t=40),
                title_text="""Specific energy for a contraction""",
                yaxis=dict(
                    title="Depth &nbsp; <i>y</i> [ft]",
                    range=[0, 5],
                    showspikes=True,
                    **axis_format,
                ),
                xaxis=dict(
                    title="Specific energy &nbsp; <i>E</i> [ft]",
                    range=[0, 5],
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

        st.markdown(
            R"""
            ************
            ## 🪜 Steps
            """
        )
        st.pyplot(draw_step())
        
        st.markdown(
            R"""
            Assuming that the energy losses through the step are negligible,

            $$
                E_1 = E_2 + \Delta z
            $$

            With $y_1$ and $Q$, $y_2$ can be predicted given a change in the
            bottom elevation (i.e., $\Delta z$).

            $$
                y_1 + \dfrac{Q^2}{2gA_1^2} = y_2 + \dfrac{Q^2}{2gA_2^2} + \Delta z
            $$

            The discharge is the same in the two sections, but the cross-sectional area
            will differ as the depth changes. 

            """
        )

        cols = st.columns([2, 1])
        with cols[1]:  ## Controls for plot
            discharge = st.slider("$Q$ [ft³/s]", 1.0, 100.0, 60.0, 0.1, key="Q_step")
            width = st.slider("$b$ [ft]", 0.1, 15.0, 6.0, 0.1)

            st.markdown("##### Section 1")
            depth_1 = st.slider("$y_1$ [ft]", 0.1, 5.0, 2.5, 0.1, key="y_1(step)")

            depth = np.geomspace(0.01, 10, 100)
            specific_energy_1 = specific_energy_calc(depth, discharge, width)
            ic_1 = np.argmin(specific_energy_1)
            E_1 = specific_energy_calc(depth_1, discharge, width)

            st.markdown("##### Section 2")
            step_height = st.slider(r"$\Delta z$ [ft]", 0.0, 1.0, 0.1, 0.01)

        with cols[0]:  ## Specific energy plot for steo
            fig = go.Figure()

            hovertemplate_eplot = "<i><b>E</b></i> = %{x:.1f} ft <br>y = %{y:.1f} ft"
            fig.add_trace(
                go.Scatter(  ## Section 1
                    x=specific_energy_1,
                    y=depth,
                    name="E(y)",
                    legendgroup="Section",
                    legendgrouptitle_text="Section",
                    hovertemplate=hovertemplate_eplot,
                    line=dict(width=5, color="purple"),
                )
            )

            fig.add_trace(  ## Critical point Section 1
                go.Scatter(
                    x=[specific_energy_1[ic_1]],
                    y=[depth[ic_1]],
                    name="y<sub>c, 1</sub>",
                    legendgroup="Section",
                    mode="markers",
                    hovertemplate=hovertemplate_eplot,
                    marker=dict(
                        size=20,
                        color="purple",
                        opacity=0.7,
                        line=dict(color="MediumPurple", width=2),
                    ),
                )
            )

            fig.add_vline(
                x=E_1,
                y0=0,
                y1=0.75,
                line=dict(dash="dot", width=1),
                annotation=dict(
                    text="<b>E</b>",
                    font_size=20,
                ),
                annotation_position="bottom right",
            )

            fig.add_hline(
                y=depth_1,
                line=dict(dash="dot", width=1),
                annotation=dict(
                    text="<b>y<sub>1</sub></b>",
                    font_size=20,
                ),
                annotation_position="top left",
            )

            fig.add_vline(
                x=E_1 - step_height,
                annotation=dict(
                    text="<b>E - Δz</b>",
                    font_size=20,
                ),
                annotation_position="top left",
                line=dict(dash="longdashdot", width=2, color="green"),
            )

            fig.update_layout(
                height=600,
                margin=dict(t=40),
                title_text="""Specific energy for a contraction""",
                yaxis=dict(
                    title="Depth &nbsp; <i>y</i> [ft]",
                    range=[0, 5],
                    showspikes=True,
                    **axis_format,
                ),
                xaxis=dict(
                    title="Specific energy &nbsp; <i>E</i> [ft]",
                    range=[0, 5],
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

        st.markdown(
            R"""
            ************
            ### ⌛ Choking

            If the specific energy upstream is less than the required to pass through
            a given section, it will have to adjust itself by either:
            
            - Decreasing its discharge
            - Increasing its specific energy

            """
        )

    elif option == "Jumps and momentum conservation":
        st.header("Hydraulic jumps")
        
        cols = st.columns(2)

        with cols[0]:
            url = "https://www.youtube.com/watch?v=xTXQKeSZbGE"
            st.video(url)
            st.caption(f"Source: [youtube.com/@a-thaksalawa2483]({url})")

        with cols[1]:
            with st.expander("Experiment with dam:"):
                url = "https://www.youtube.com/watch?v=VU7UEiO6ijA"
                st.video(url)
                st.caption(f"Source: [youtube.com/@WakaWakaWakaW]({url})")

            with st.expander("Experiment in a flume:", expanded=True):
                url = "https://www.youtube.com/watch?v=uz7d_1KnbPM"
                st.video(url)
                st.caption(f"Source: [youtube.com/@WakaWakaWakaW]({url})")

        st.markdown(
            R"""
            *******
            The goal of a hydraulic jump is to disipate energy
            in a short lenght.
            """
        )
        st.pyplot(draw_hydraulic_jump())
        
        st.markdown(
            R"""
            ******
            ### Momentum conservation

            Linear momentum is defined as:
            
            $$
                \mathbf{F} = \dfrac{d \mathbf{p}}{dt}
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$\mathbf{F}$| Force | Mass · Acceleration |
            |$\mathbf{p} = mV$| Linear momentum | Mass · Velocity  |
            |$t$| Time | Time  |

            &nbsp;

            Momentum is conserved if:
            $$
                \begin{array}{rl}
                \dfrac{d \mathbf{p}}{dt} = & 
                \textsf{Momentum transfer} \\
                & + \;
                \textsf{External forces}
                \end{array}
            $$


            In an open channel flow, momentum and external forces in the flow
            direction come from:

            |Source|Equation|
            |:----||:-------|
            |Mass flow rate |$m V = \rho \, Q \, V$ |
            |Pressure distribution | $F_p = p \, A = \gamma \, Y_C \, A$ |
            |Weight | $F = m g = \Delta x \, A \sin{\theta}$
            |Friction with the channel walls |$F_f$|
            |Obstacles |$F_e$|

            &nbsp;

            Between sections 1 (upstream) and 2 (downstream), momentum balance is
            
            $$
                \dfrac{d \mathbf{p}}{dt} =
                \rho \, Q \, \left(V_1 - V_2 \right)
                +
                \gamma \left(A_1\,Y_{C_1} - A_1\,Y_{C_1}\right)
                +
                \Delta x \, A \sin{\theta}
                -
                F_f - F_e
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$Q$| Discharge | Volume/Time |
            |$A$| Cross-sectional area | Area |
            |$Y_C$| Depth to the centroid of the flow section | Length |
            |$\gamma = \rho g$| Fluid specific weight | Force/Volume |

            &nbsp;

            For a permanent flow, $\dfrac{d \mathbf{p}}{dt} = 0$. Also, 
            replacing $V = Q/A$, and dividing by $\gamma$

            $$
                \dfrac{Q^2_1}{gA_1}
                + \ A_1 \, Y_{C_1} 
                =
                \dfrac{Q^2_2}{gA_2}
                + A_2 \, Y_{C_2}
                - \dfrac{F_f}{\gamma}
                - \dfrac{F_e}{\gamma}
                + \Delta x \, S_w \, \dfrac{A_2 + A_1}{2}
            $$
            
            If the longitudinal distance is short enough, the external force
            due friction $F_f$ with the channel and the weight of the mass of water can be ignored.
            Also, if there are no obstacles, the momentum equation conservation
            can be reduced to

            $$
                \dfrac{Q^2_1}{gA_1}
                + \ A_1 \, Y_{C_1} 
                =
                \dfrac{Q^2_2}{gA_2}
                + A_2 \, Y_{C_2}
            $$

            ****
            ### Specific force (or specific momentum)

            It is defined in a section as

            $$
                M = \dfrac{Q^2}{gA} + A \, Y_C
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$M$| Specific momentum | Volume |
            |$Q$| Discharge | Volume/Time |
            |$A$| Cross-sectional area | Area |
            |$Y_C$| Depth to the pressure distribution centroid | Length |
            
            &nbsp;

            Even though specific energy is not conserved,

            $$
                E_1 = E_2 + \Delta E
            $$

            The specific momentum should be,

            $$
            \begin{array}{rcl}
                M_1 &=& M_2 \\
                \\
                \dfrac{Q^2}{gA_1} + A_1 \, Y_{C_1} &=& \dfrac{Q^2}{gA_2} + A_2 \, Y_{C_2}
            \end{array}
            $$

            The pair of depths that satisfy this equation are called **conjugate** depths.

            ****
            ### Specific force diagram

            """
        )

        with st.echo():

            def specific_force_calc(y, Q, b, units="SI"):
                A = y * b
                g = 32.2 if units == "BG" else 9.81
                Y_c = y / 2
                return A * Y_c + np.power(Q, 2) / (g * A)

        st.divider()

        cols = st.columns([2, 1])

        with cols[1]:  ## Controls for plot
            st.markdown("##### Diagram")
            discharge = st.slider("$Q$ [m³/s]", 0.4, 40.0, 15.0, 0.1)
            width = st.slider("$b$ [m]", 0.1, 15.0, 3.0, 0.1)
            depth_1 = st.slider("$y_1$ [m]", 0.1, 5.0, 0.40, 0.1)

            depth_2_guess = st.slider(r"$y_{2,\textsf{Guess}}$ [m]", 0.1, 5.0, 5.0, 0.1)

            depth = np.geomspace(0.01, 10, 100)
            specific_force_1 = specific_force_calc(depth, discharge, width)
            ic_1 = np.argmin(specific_force_1)

            M_1 = specific_force_calc(depth_1, discharge, width)

            solver_container = st.empty()

        st.markdown("#### 🧮 Calculate the conjugate depth using `scipy.root`")

        with st.echo():
            from scipy.optimize import root

            def conjugate_depth(y2, y1, Q, b):
                M_1 = specific_force_calc(y1, Q, b)
                M_2 = specific_force_calc(y2, Q, b)
                return M_1 - M_2

            depth_2 = root(
                conjugate_depth,
                x0=depth_2_guess,
                args=(
                    depth_1,
                    discharge,
                    width,
                ),
            )

            if depth_2.success:
                with solver_container.container():
                    "Conjugated depth"
                    st.metric(r"$y_2$ [m]", f"{depth_2.x[0]:.2f} m")

        with cols[0]:
            fig = go.Figure()

            hovertemplate_Mplot = "<i><b>M</b></i> = %{x:.1f} m³ <br>y = %{y:.1f} m"
            fig.add_trace(
                go.Scatter(  ## Section 1
                    x=specific_force_1,
                    y=depth,
                    name="<i>M(y)</i>",
                    hovertemplate=hovertemplate_Mplot,
                    line=dict(width=5, color="purple"),
                )
            )

            fig.add_trace(  ## Critical point Section 1
                go.Scatter(
                    x=[specific_force_1[ic_1]],
                    y=[depth[ic_1]],
                    name="Critical <br>depth <i>y<sub>c</sub><i>",
                    legendgroup="Section1",
                    mode="markers",
                    hovertemplate=hovertemplate_Mplot,
                    marker=dict(
                        size=20,
                        color="purple",
                        opacity=0.7,
                        line=dict(color="MediumPurple", width=2),
                    ),
                )
            )

            fig.add_vline(
                x=M_1,
                annotation=dict(text="<b>M</b>", font_size=20),
                line=dict(dash="dot", width=1),
            )

            fig.add_hline(  ## Depth 1
                y=depth_1,
                annotation=dict(text="<b>y<sub>1</sub></b>", font_size=20),
                line=dict(dash="dot", width=1),
            )

            fig.add_hline(  ## Depth 2
                y=depth_2.x[0],
                annotation=dict(text="<b>y<sub>2</sub></b>", font_size=20),
                line=dict(dash="dot", width=1),
            )

            fig.update_layout(
                height=600,
                margin=dict(t=70),
                title_text="""Specific force diagram <br>Hydraulic jump in rectangular section""",
                yaxis=dict(
                    title="Depth &nbsp; <i>y</i> [m]",
                    range=[0, 5],
                    showspikes=True,
                    **axis_format,
                ),
                xaxis=dict(
                    title="Specific force &nbsp; <i>M</i> [m³]",
                    range=[0, 50],
                    showspikes=True,
                    **axis_format,
                ),
                legend=dict(
                    # title="",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="bottom",
                    y=depth[ic_1] / 5.0,
                    xanchor="right",
                    x=0.96,
                ),
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(fig, use_container_width=True)

    elif option == "Uniform flow":

        st.markdown(        
            R"""
            - The water depth $y$, the cross-sectional area $A$, the discharge $Q$ and the velocity profile $V(y,z)$
            remain constant over the channel lenght
            - The EGL, water surface and channel bottom are parallel
            $$
                S_0 = S_w = S_e
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$S_0$| Channel bottom slope | - |
            |$S_w$| Water surface slope| - |
            |$S_e$| Energy line gradient | - |

            *****
            ### Chézy formula

            $$
                V = C_{\textsf{Chézy}} \, \sqrt{R_h \, S_e}
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$V$| Mean velocity | Length/Time |
            |$C_{\textsf{Chézy}}$| Chézy's resistance factor | - |
            |$R_h$| Hydraulic radius | Length |
            |$S_e$| Energy line gradient | - |


            *****
            ### Manning equation

            $$
                V = \dfrac{k_\textsf{M}}{n} \, R_h^{\frac{2}{3}} \, \sqrt{S_e}
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$V$| Mean velocity | Length/Time |
            |$k_\textsf{M} = \bigg\{ \substack{1.00 \, \mathrm{\sqrt[3]{m}/s} \\ \\ 1.49 \, \mathrm{\sqrt[3]{ft}/s}} $| Unit conversion factor.  | Length/Time |
            |$n$| Manning coefficient of roughness | - |
            |$R_h$| Hydraulic radius | Length |
            |$S_e$| Energy line gradient | - |

            &nbsp;

            In terms of discharge,

            $$
                Q = \dfrac{k_\textsf{M}}{n} \,A \, R_h^{\frac{2}{3}}\sqrt{S_e}
            $$
            """
        )
        
        st.info(
            R"""
            - Who was Antoine de Chézy? 🇫🇷
            - How is Chézy formula derived?
            - Who was Robert Manning? 🇮🇪
            """,
            icon="🏞️",
        )

        st.markdown(
            R"""
            *******
            ## Normal depth $y_n$
            
            Given a discharge $Q$ and a channel bottom slope $S_0$, the normal depth $y_n$
            satisfies the normal flow equation.

            ### For a rectangular section:
            """
        )

        cols = st.columns([1.5, 2])

        with cols[0]:  ## Channel options
            st.markdown("#### Parameters")

            width = st.number_input(
                "Width -- $b$ [m]", 0.1, 50.0, 3.0, 1.0, format="%.2f"
            )
            discharge = st.number_input(
                "Discharge -- $Q$ [m³/s]", 0.1, 200.0, 25.3, 1.0, format="%.1f"
            )
            n_manning = st.number_input(
                "Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.022, 0.001, format="%.3f"
            )
            slope = st.number_input(
                "Bottom slope -- $S_0$ [-]",
                0.0001,
                0.1000,
                0.0410,
                0.0001,
                format="%.4f",
            )
            initial_guess = st.number_input(
                "Initial guess for $y_n$", 0.01, 50.0, 1.2, format="%.2f"
            )
            method = st.selectbox("Root finding method:", ["hybr", "lm"])

        with cols[1]:  ## Function def
            st.markdown("#### Define equation to solve")
            with st.echo():

                def solve_normal_depth_rect_channel(
                    depth: float,
                    width: float,
                    discharge: float,
                    n_manning: float,
                    slope: float,
                ):
                    k = 1.0  ## SI Units
                    area = width * depth
                    wetted_perim = width + 2 * depth
                    hydr_radius = area / wetted_perim
                    calculated_discharge = (
                        k
                        / n_manning
                        * area
                        * np.power(hydr_radius, 2 / 3)
                        * np.sqrt(slope)
                    )

                    return discharge - calculated_discharge

            st.markdown("#### Call `scipy.root`")
            with st.echo():
                from scipy.optimize import root

                normal_depth = root(
                    solve_normal_depth_rect_channel,
                    x0=initial_guess,
                    args=(width, discharge, n_manning, slope),
                    method=method,
                )

        with cols[0]:
            st.divider()
            if normal_depth.success:
                st.metric(R"*Solved* $\; y_n$", f"{normal_depth.x[0]:.2f} m")
            else:
                st.error(
                    R"""
                    Something went wrong... 
                    try changing the initial guess for $y_n$ or the root-finding method.
                    """,
                    icon="🧪",
                )

        st.markdown(
            R"""
            *****
            ## Critical slope $S_c$
            
            It is the channel bottom slope that satisfies that
            
            $$
                y_c = y_n
            $$
            
            """
        )

    elif option == "Gradually varied flow":
        st.markdown(    
            R"""
            ## Gradually Varied Flow (GVF)
            
            Changes in water depth occur over long distances.  The total energy of the
            flow in a given section is

            $$
                H = z + y + \dfrac{Q^2}{2g\,A^2}
            $$

            Differentiating along the longitudinal distance $x$,

            $$
                \dfrac{dH}{dx} = \dfrac{dz}{dx} + \dfrac{dy}{dx} + \dfrac{-Q^2}{g\,A^3}\dfrac{dA}{dx}
            $$

            Rearanging for the water surface slope $dy/dx$,
            
            $$
                \dfrac{dy}{dx} = \dfrac{\dfrac{dH}{dx} - \dfrac{dz}{dx}}{1 - \dfrac{Q^2\,T}{g\,A^3}}
            $$ 

            | Parameter | Description   | Units  |
            |:---------:|:--------:|:------------------:|
            |$dy/dx = S_w$  | Slope of the water surface  | - | 
            |$dz/dx = S_0$  | Slope of the bottom channel | - | 
            |$dH/dx = S_e$  | Slope of the EGL | - | 
            |$Q$  | Discharge | Volume/Time | 
            |$A$  | Cross-sectional area | Area | 
            |$T$  | Top width | Length | 

            &nbsp;

            Or, 

            $$
                \dfrac{dy}{dx} = \dfrac{S_e - S_0}{1 - \mathsf{F_r}^2}
            $$

            &nbsp;

            Since the changes in depth occur in short distances, it can be assumed that
            $S_e$ could be calculated using a normal flow equation (i.e., Manning equation).
            
            :red[**$S_e$ is always negative** because energy is always lost.] 
            
            :orange[$S_0$ is usually negative, but there are cases of **adverse** slopes, 
            i.e., $S_0 > 0$]

            :blue[**Uniform flow** occur when $S_e = S_0$, thus the water depth remains
            constant, i.e., $dy/dx = 0$]

            *****

            ## Surface water profiles

            $$
            \def\arraystretch{1.8}
            \begin{array}{r|c:c}
                & \textsf{🐢} & \textsf{🐇} \\
                \textsf{Flow classification} & \textsf{Subcritical} & \textsf{Supercritical} \\
            
                \hdashline
                \textsf{Froude number} & \mathsf{F_r} < 1.0 & \mathsf{F_r} > 1.0 \\
                & \quad 1 - \mathsf{F_r}^2 > 0.0 \quad & \quad 1 - \mathsf{F_r}^2 < 0.0 \quad \\
                \hline
                S_0 > 0 & {dy}/{dx} < 0 & {dy}/{dx} > 0 \\
                \hdashline
                S_e - S_0 < 0 & {dy}/{dx} < 0 & {dy}/{dx} > 0 \\
                \hdashline
                S_e - S_0 > 0 & {dy}/{dx} > 0 & {dy}/{dx} < 0 \\
                
                \hline
            \end{array}
            $$
            
            ******
            """
        )

        cols = st.columns([1, 2])

        with cols[0]:
            container = st.empty()

            S0 = st.slider(r"$S_0$", -0.10, 0.10, -0.01, 0.01, format="%.2f")
            Se = st.slider(r"$S_e$", -0.10, -0.01, -0.10, 0.01, format="%.2f")
            Fr = st.slider(r"$\mathsf{F_r}$", 0.1, 2.0, 0.1, 0.1, format="%.2f")

            def sign_emoji(number):
                if isinstance(number, float):
                    if number > 0:
                        emoji = "➕"
                    elif number < 0:
                        emoji = "➖"
                    elif number == 0:
                        emoji = "0"
                    return emoji

                else:
                    return None

            numerator = sign_emoji(Se - S0)
            denominator = sign_emoji(1.0 - Fr**2)

            with container.container():
                st.markdown(
                    rf"""
                    $$
                        \dfrac{{dy}}{{dx}}
                        =
                        \dfrac{{S_e - S_0}}{{1 - \mathsf{{F_r}}^2}}
                        =
                        \dfrac{{ {numerator} }}{{ \textbf{{{denominator}}} }}
                    $$
                    """
                )

        with cols[1]:
            if Fr == 1:
                _, lilcol, _ = st.columns([1, 2, 1], vertical_alignment="center")
                with lilcol:
                    
                    st.error(
                        R"""
                        ## 🛑 **Critical flow**
                        $$ 
                            \mathsf{F_r} = 1.0 
                        $$
                        """
                    )

            else:
                st.pyplot(FGV_intuition(S0, Se, Fr))

        st.markdown(
            R"""
            *****

            ## Slope classification

            |Symbol| Name | In terms of bottom slope | In terms of depth |
            |:---:|:---|:----:|:---:|
            |$\mathtt{M}$| Mild | $S_0 < S_c$ | $y_n > y_c$ |
            |$\mathtt{C}$| Critical | $S_0 = S_c$ | $y_n = y_c$ |
            |$\mathtt{S}$| Steep | $S_0 > S_c$ | $y_n < y_c$ |
            |$\mathtt{H}$| Horizontal | $S_0 = 0$ | No normal flow |
            |$\mathtt{A}$| Adverse | $S_0 > 0$ | No normal flow |

            &nbsp;

            """
        )

    elif option == "Rivers":
        st.subheader(R"🏞️ $\quad \textsf{Water} + \textsf{sediments} + \textsf{movement} = \textsf{river}$", anchor=False)

        url = "https://upload.wikimedia.org/wikipedia/commons/a/ad/Missouri-River-Morning-Drone-Shot.webm"
        st.caption(
            "**Missouri River:**<br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.video(url)

        url = "https://upload.wikimedia.org/wikipedia/commons/e/ed/Framrusti_river_02.webm"
        st.caption(
            "**Steep-slope:**<br>" + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.video(url)

        url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/38confpigeoncynsnakegulch.073009_l.jpg"
        st.caption(
            "**Grand Canyon:** Erosion through layers of sedimentary rocks.<br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://live.staticflickr.com/1567/23631659763_498c8ed16d_o_d.jpg"
        st.caption(
            "**Meandering river:** What is the direction of the flow?.<br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://www.publicdomainpictures.net/pictures/30000/velka/fast-flowing-river.jpg"
        st.caption(
            "**Fast flowing river:** Sediment size can vary substantially. <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://live.staticflickr.com/1568/24232357896_9d9bc78f9c_o_d.jpg"
        st.caption(
            "**River faces into ocean:** What happened with the sediments? <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://upload.wikimedia.org/wikipedia/commons/2/2b/120408_Pheriche_Pano_4k.jpg"
        st.caption(
            "**Rio Tamaya (Perú):** Constantly channel section and slope <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = (
            "https://upload.wikimedia.org/wikipedia/commons/4/49/Rio_Negro_meanders.JPG"
        )
        st.caption(
            "**Khumbu Khola valley (Nepal):** Valley width v. flooding plain width v. channel width <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://upload.wikimedia.org/wikipedia/commons/3/31/Sandbar_on_the_Mississippi%2C_New_Orleans.jpg"
        st.caption(
            "**Mississippi River (New Orleans, LA):** Sandbar <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://upload.wikimedia.org/wikipedia/commons/e/eb/SantaremTejo.jpg"
        st.caption(
            "**Tejo River (Portugal):** More sandbars <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = "https://upload.wikimedia.org/wikipedia/commons/3/35/Takato_Dam_discharge.jpg"
        st.caption(
            "**高遠ダム Takatō Dam (Japan):** Sediments are deposited behind the dam. Erosion exacerbates downstream <br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        url = (
            "https://upload.wikimedia.org/wikipedia/commons/3/31/StauseeMooserboden.jpg"
        )
        st.caption(
            "**Stausee Mooserboden**, seen from Hoher Tenn, Austria.<br>"
            + f"*Source:* [*{urlparse(url).hostname}*]({url})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)

        st.divider()
        _, col, _ = st.columns([1, 3, 1])
        with col:
            url = "https://ascelibrary.org/doi/book/10.1061/9780784408148"
            st.markdown(
                rf"""
                Also check:

                ⏺ Garcia, Marcelo. (Ed.). (2008). <br>
                **Sedimentation Engineering: Processes, Measurements, Modeling and Practice**. <br>
                *American Society of Civil Engineers.* <br>
                DOI: [10.1061/9780784408148]({url})
                
                """,
                unsafe_allow_html=True,
            )

            url = "https://ascelibrary.org/doi/book/10.1061/9780784408230"
            st.markdown(
                rf"""
                ⏺ Vanoni, V.A. (Ed.). (2006). <br>
                **Sedimentation Engineering**. <br>
                *American Society of Civil Engineers.* <br>
                DOI: [10.1061/9780784408230]({url})
                
                """,
                unsafe_allow_html=True,
            )

    elif option == "Sediments":
        st.markdown(
            R"""
            ## Sediment classification

            ### 📏 By size
            """
        )

        tabs = st.tabs(
            [
                "Boulders",
                "Gravel",
                "Sand",
                "Silt",
                "Clay",
            ]
        )

        with tabs[0]:  # Boulders
            url = "https://upload.wikimedia.org/wikipedia/commons/0/00/A_large_boulder_in_the_river_-_geograph.org.uk_-_4027686.jpg"
            source = "https://www.geograph.org.uk/photo/4027686"
            st.caption(
                "**Water of Tanar (Scotland)**. A large boulder in the river<br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with tabs[1]:  # Gravel
            url = "https://s0.geograph.org.uk/geophotos/01/06/64/1066461_89c35f88.jpg"
            source = "https://www.geograph.org.uk/photo/1066461"
            st.caption(
                "**River Brent (England)**. A gravel bar<br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with tabs[2]:  # Sand
            url = "https://upload.wikimedia.org/wikipedia/commons/3/3b/Sand_at_the_banks_of_Arno_river.jpg"
            source = "https://commons.wikimedia.org/wiki/File:Sand_at_the_banks_of_Arno_river.jpg"
            st.caption(
                "**Arno River (Italy)**. A sand bar<br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with tabs[3]:  # Silt
            url = "https://upload.wikimedia.org/wikipedia/commons/c/c3/Mossy_Cave_area_-_Bryce_Canyon_National_Park.jpg"
            source = "https://commons.wikimedia.org/wiki/File:Mossy_Cave_area_-_Bryce_Canyon_National_Park.jpg?uselang=fr"
            st.caption(
                "**Bryce Canyon NP (USA)**. Mudflow <br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with tabs[4]:  # Clay
            url = "https://upload.wikimedia.org/wikipedia/commons/b/bb/Sediment_Spews_from_Connecticut_River.jpg"
            source = "https://earthobservatory.nasa.gov/images/52059/sediment-spews-from-connecticut-river"
            st.caption(
                "**Conneticut River** [left], **Thames River** [right] **(USA)**. Suspended sediments<br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        st.markdown(
            R"""
            ****
            ### 🚚 By transport mechanism

            $$
                \textsf{Rouse number:} \quad \mathsf{P} = \dfrac{\textsf{Settling}}{\textsf{Resuspension}} = \dfrac{v_s}{\kappa u_*}
            $$
            
            | Parameter | Description   | Units  |
            |:---------:|:--------:|:------------------:|
            |$ \mathsf{P} $  | Rouse number  | - | 
            |$ v_s $  | Settling velocity  | Length/Time 
            |$ \kappa = 0.41 $  | von Kármán constant  | Length/Time | 
            |$ u_* $  | Shear velocity  | Length/Time | 
            
            &nbsp;

            """
        )

        cols = st.columns(2)

        with cols[0]:
            st.markdown("""#### 🛏️ Bed load""")
            url = "https://www.youtube.com/watch?v=EWRcyq6vnyc"
            st.caption(f"Source: [youtube.com/@cuboulder]({url})")
            st.video(url)

        with cols[1]:
            st.markdown("""#### 🎈 Suspended load""")
            url = "https://upload.wikimedia.org/wikipedia/commons/e/e3/Bl%C5%A1anka_Suspended_Load.jpg"
            source = "https://en.wikipedia.org/wiki/Suspended_load#/media/File:Bl%C5%A1anka_Suspended_Load.jpg"
            st.caption(
                "**Suspended sediment in a river**. Suspended sediments<br>"
                + f"*Source:* [*{urlparse(source).hostname}*]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

    elif option == "Lane's diagram":
        
        st.markdown(
            R"""

            $$
                \underbrace{q_s \, d_{50}}_{\substack{\textsf{Sediment} \\ \textsf{transport} }}
                \quad \propto \quad
                \underbrace{Q_w \, S_0}_{\textsf{Water flow}}
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$q_s$| Sediment transport rate | Area/Time |
            |$Q_w$| Water discharge | Volume/Time |
            |$d_{50}$  | Sediment size | Length |
            |$S_0$| Stream slope  | - |

            &nbsp;

            """
        )

        with st.expander("**⚖️ Lane's balance**", expanded=True):
            url = "https://www.researchgate.net/profile/Massimo-Rinaldi-2/publication/283538764/figure/fig14/AS:613448840929287@1523269009117/Lanes-balance-one-of-the-most-recognized-conceptual-models-and-graphics-in-Fluvial.png"
            st.image(url, use_column_width=True)
            st.caption(f"Source: [researchgate.net / *Rinaldi et al. 2015*]({url})")

    elif option == "Shear stress":
        img = "./book/assets/img/ShieldsDiagram.png"
        st.caption(
            "**Shields Diagram** <br> Source: [Shields, 1936](https://repository.tudelft.nl/islandora/object/uuid:a66ea380-ffa3-449b-b59f-38a35b2c6658?collection=research)",
            unsafe_allow_html=True,
        )
        st.image(img, use_column_width=True)

        st.markdown(
            R"""
            *****
            ### Shields parameter

            Movement of bed sediments occur when the shear stress exerted by the water on the bed 
            is greater than the resistance of the sediments to remain in place.

            $$
                \tau_* = \dfrac{\textsf{Flow stress}}{\textsf{Bed resistance}} = \dfrac{\tau_b}{(\gamma_s - \gamma) \, d}
            $$
            
            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$\tau_*$| Shields parameter | - |
            |$\tau_b$| Tractive shear stress | Force/Area |
            |$\gamma_s$| Specific weight of sediment | Force/Volume |
            |$\gamma$| Specific weight of water | Force/Volume |
            |$d$| Characteristic particle size | Length |
            
            &nbsp;

            $$
            \begin{cases}
            \begin{array}{rcl}
                \textsf{Motion:} &\quad& \tau_* > \tau_{c*}
                \\
                \textsf{No motion:} &\quad&  \tau_* < \tau_{c*}
            \end{array}
            \end{cases}
            $$

            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$\tau_*$| Shields parameter | - |
            |$\tau_{c*}$| Critical Shields parameter | - |
            
            &nbsp;

            $$
                \tau_b = \gamma R_h S_0
            $$

            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$R_h$| Hydraulic radius | Length |
            |$S_0$| Channel slope | - |

            &nbsp;

            ### Sediment Reynolds number

            $$
                R_{e*} = \dfrac{u_* \, d}{\nu}
            $$

            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$R_{e*}$| Sediment Reynolds number | - |
            |$u_*$| Shear velocity | Length |
            |$d$| Particle size | Length |
            |$\nu$| Kinematic viscosity | Length²/Time |

            &nbsp;
            
            $$
                u_* = \sqrt{\dfrac{\tau_b}{\rho}}
            $$

            ### Fitting Shields data to a curve
            
            $$
                \tau_{c*} = 0.22 R_{e*}^{-0.6} + 0.06 \exp{\left( -17.77 R_{e*}^{-0.6} \right)}
            $$ 


            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$\tau_{c*}$| Critical Shields parameter | - |
            |$R_{e*}$| Sediment Reynolds number | - |

            &nbsp;

            ### Stokes law & settling velocity 

            $$
                v_s = \dfrac{d^2}{18 \nu}\left(\dfrac{\gamma_s - \gamma}{\gamma}\right)
            $$

            |Parameter|Description|Units|
            |:---:|:-------|:----|
            |$d$| Characteristic particle size | Length |
            |$\gamma_s$| Specific weight of sediment | Force/Volume |
            |$\gamma$| Specific weight of water | Force/Volume |
            |$\nu$| Kinematic viscosity | Length²/Time |

            &nbsp;

            $$
            \begin{cases}
            \begin{array}{rcl}
                \textsf{Suspension:} &\quad& v_s < u_*
                \\
                \textsf{No suspension:} &\quad&  v_s > u_*
            \end{array}
            \end{cases}
            $$

            ****
            """
        )

        st.caption(
            R"""
            **Parker's River sedimentation diagram** <br>
            Adapted from: [García, M. (Ed.). (2008)](https://doi.org/10.1061/9780784408148). <br>
            """,
            unsafe_allow_html=True,
        )
        st.pyplot(draw_shields())

    elif option == "~Solve IVP":
        solve_ivp()
    
    else:
        st.error("You should not be here!")


def draw_shields():
    fig, ax = plt.subplots()
    Re_star = np.geomspace(1, 1_000, 100)
    tau_crit = 0.22 * np.power(Re_star, -0.6) + 0.06 * np.exp(
        -17.77 * np.power(Re_star, -0.6)
    )
    tau_susp = np.exp(
        -2.891394
        + 0.95296 * np.log(Re_star)
        - 0.056835 * np.power(np.log(Re_star), 2)
        - 0.002892 * np.power(np.log(Re_star), 3)
        + 0.000245 * np.power(np.log(Re_star), 4)
    )

    ax.plot(Re_star, tau_crit, c="tab:blue")
    ax.text(
        Re_star[-45],
        tau_crit[-45] + 5e-3,
        "Motion",
        ha="center",
        va="bottom",
        c="tab:blue",
    )
    ax.text(
        Re_star[-45],
        tau_crit[-45] - 5e-3,
        "No motion",
        ha="center",
        va="top",
        c="tab:blue",
    )

    ax.plot(Re_star, tau_susp, ls="dashed", c="darkorange")
    ax.text(
        Re_star[-15],
        tau_susp[-15] + 2e-1,
        "Suspension",
        ha="center",
        va="bottom",
        c="darkorange",
        rotation=10,
    )
    ax.text(
        Re_star[-15],
        tau_susp[-15] - 2e-1,
        "No suspension",
        ha="center",
        va="top",
        c="darkorange",
        rotation=10,
    )

    ax.set_xscale("log")
    ax.set_xlim(1, 1_000)
    ax.set_xlabel(r"$R_{e*} = \dfrac{u_{*} \, d}{\nu}$", fontsize=14)

    ax.set_yscale("log")
    ax.set_ylim(1e-2, 8.0)
    ax.set_ylabel(r"$\tau_{*} = \dfrac{\tau_b}{(\gamma_s - \gamma) \, d}$", fontsize=14)
    ax.grid(True, which="both", alpha=0.6)

    return fig


def draw_contraction():
    side_down = Side(x=np.array([0, 4, 12, 15]), y=np.array([-3, -3, -2, -2]))

    side_up = Side(x=side_down.x, y=-side_down.y)

    water_surface = Side(x=side_down.x, y=np.array([2, 2, 1, 1]))

    fig, axs = plt.subplots(
        2, 1, sharex=True, figsize=[8, 10], gridspec_kw=dict(hspace=-0.2)
    )

    ax = axs[0]  ## Profile view
    ax.set_ylabel("Profile view", loc="center")

    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0],
        water_surface.y[0] + 0.1,
        r"HGL",
        ha="left",
        fontdict=dict(size=10, color="navy"),
    )

    ## EGL
    ax.plot(water_surface.x, [3.5] * 4, c="mediumseagreen", ls="dashed")
    ax.text(
        water_surface.x[0],
        3.5 + 0.1,
        r"EGL",
        ha="left",
        fontdict=dict(size=10, color="mediumseagreen"),
    )

    # Datum
    ax.axhline(-2, lw=1, color="k", ls="dashed", zorder=0)
    ax.text(1.0, -2 + 0.1, r"Datum", ha="center", fontdict=dict(size=8))

    # Sections annotations
    for i, x in enumerate(water_surface.x[1:3], start=1):
        ## Sections
        ax.plot([x] * 2, [-4, 4], ls="dotted", lw=1, c="gray")
        ax.text(
            x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray")
        )

        ## Depth
        ax.plot(
            [x] * 2,
            [-2, water_surface.y[i]],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (water_surface.y[i] - 2) / 2,
            rf"$y_{i}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

        ## Velocity head
        ax.plot(
            [x] * 2,
            [water_surface.y[i], 3.5],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (water_surface.y[i] + 3.5) / 2,
            rf"$\dfrac{{Q^2}}{{2gA^2_{i}}}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

    # Channel bottom
    ax.axhline(
        y=-2,
        lw=1.5,
        c="gray",
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=-45, spacing=6, length=3)
        ],
    )

    ax.text(
        water_surface.x[-1],
        -2 + 0.1,
        r"Channel bottom",
        ha="right",
        fontdict=dict(size=8, color="0.2"),
    )

    # ax.fill_between(water_surface.x, -2, -2 - 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")

    # Final touches
    ax.set_ylim(-3, 5.0)

    #####################################
    ax = axs[1]  ## Plan view
    ax.set_ylabel("Plan view", loc="center")

    ## Channel borders
    ax.plot(
        side_down.x,
        side_down.y,
        lw=1.5,
        c="gray",
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=-45, spacing=6, length=3)
        ],
    )

    # ax.fill_between(side_down.x, side_down.y, side_down.y - 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")

    ax.plot(
        side_up.x,
        side_up.y,
        lw=1.5,
        c="gray",
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=45, spacing=6, length=3)
        ],
    )

    # ax.fill_between(side_up.x, side_up.y, side_up.y + 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")

    ## Section annotations
    for i, x in enumerate(side_down.x[1:3], start=1):
        ## Sections
        ax.plot([x] * 2, [-4, 4], ls="dotted", lw=1, c="gray")
        ax.text(
            x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray")
        )

        ## Width
        ax.plot(
            [x] * 2,
            [side_down.y[i], side_up.y[i]],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            0,
            rf"$b_{i}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

    # Final touches
    # ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_ylim(-5.0, 5.0)

    # Final touches for all axes
    for ax in axs:
        ax.set_xlim(side_down.x[0], side_down.x[-1])
        ax.set_aspect("equal")

        # ax.grid(True, color="lightgray")
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        ## Flow direction
        ax.text(
            side_down.x.mean(),
            0,
            r"$Q$",
            ha="left",
            va="center",
            size=12,
            bbox=dict(boxstyle="rarrow,pad=0.3", fc="cornflowerblue", alpha=0.5, lw=0),
        )
    return fig


def draw_step():
    bottom = Side(x=np.array([0, 4, 12, 15]), y=np.array([-2, -2, -1, -1]))

    water_surface = Side(x=bottom.x, y=np.array([2, 2, 0.5, 0.5]))

    fig, ax = plt.subplots()
    ax.set_ylabel("Profile view", loc="center")

    # Datum
    ax.axhline(-2, lw=1, color="k", ls="dashed", zorder=2)
    ax.text(bottom.x[-1], -2 + 0.1, r"Datum", ha="right", fontdict=dict(size=8))

    ## Bottom
    ax.plot(
        bottom.x,
        bottom.y,
        c="0.50",
        lw=1.5,
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=-45, spacing=6, length=1.3)
        ],
    )
    ax.text(
        bottom.x[0],
        bottom.y[0] + 0.1,
        r"Channel bottom",
        ha="left",
        fontdict=dict(size=8, color="0.2"),
    )

    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0],
        water_surface.y[0] + 0.1,
        r"HGL",
        ha="left",
        fontdict=dict(size=10, color="navy"),
    )

    ## EGL
    ax.plot(water_surface.x, [4] * 4, c="mediumseagreen", ls="dashed")
    ax.text(
        water_surface.x[0],
        4 + 0.1,
        r"EGL",
        ha="left",
        fontdict=dict(size=10, color="mediumseagreen"),
    )

    # Sections annotations

    ## Depth
    ax.plot(
        [bottom.x[-2]] * 2,
        [-2, bottom.y[-2]],
        marker="o",
        ms=4,
        lw=2,
        c="darkslategray",
        ls=":",
    )
    ax.text(
        bottom.x[-2] + 0.2,
        bottom.y.mean(),
        r"$\Delta z$",
        ha="left",
        va="center",
        fontdict=dict(color="darkslategray", size=12),
    )

    for i, x in enumerate(bottom.x[1:3], start=1):
        ## Sections
        ax.plot([x] * 2, [-4, 4], ls="dotted", lw=1, c="gray")
        ax.text(
            x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray")
        )

        ## Depth
        ax.plot(
            [x] * 2,
            [bottom.y[i], water_surface.y[i]],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (bottom.y[i] + water_surface.y[i]) / 2,
            rf"$y_{i}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

        ## Velocity head
        ax.plot(
            [x] * 2,
            [water_surface.y[i], 4],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (water_surface.y[i] + 4) / 2,
            rf"$\dfrac{{Q^2}}{{2gA^2_{i}}}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

    # Final touches for all axes
    ax.set_xlim(bottom.x[0], bottom.x[-1])
    ax.set_ylim(-2.5, 5)
    ax.set_aspect("equal")
    # ax.grid(True, color="lightgray")
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    ## Flow direction
    ax.text(
        bottom.x.mean(),
        0,
        r"$Q$",
        ha="left",
        va="center",
        size=12,
        bbox=dict(boxstyle="rarrow,pad=0.3", fc="cornflowerblue", alpha=0.5, lw=0),
    )
    return fig


def realistic_water(ax: plt.Axes, p: Point, size: float):
    img = get_image_as_PIL("https://cdn4.iconfinder.com/data/icons/water-waves-design/1470/tornado_blue_water_wave_spiral_hurricane_logo-512.png")
    imagebox = OffsetImage(img, zoom=size, cmap="bone_r")
    ax.add_artist(AnnotationBbox(imagebox, p, frameon=False, zorder=1))


def draw_hydraulic_jump():
    bottom = Side(
        x=np.array([0, 4, 6, 8, 10, 15]), y=np.array([-2, -2, -2, -2, -2, -2])
    )

    water_surface = Side(x=bottom.x, y=np.array([-1, -1, -1, 2, 2, 2]))

    energy_line = Side(x=bottom.x, y=np.array([5, 5, 5, 4, 4, 4]))

    fig, ax = plt.subplots()
    ax.set_ylabel("Profile view", loc="center")

    # Datum
    ax.axhline(-2, lw=1, color="k", ls="dashed", zorder=2)
    ax.text(bottom.x[-1], -2 + 0.1, r"Datum", ha="right", fontdict=dict(size=8))

    ## Bottom
    ax.plot(
        bottom.x,
        bottom.y,
        c="0.50",
        lw=1.5,
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=-45, spacing=6, length=1.5)
        ],
    )

    ax.text(
        bottom.x[0],
        bottom.y[0] + 0.1,
        r"Channel bottom",
        ha="left",
        fontdict=dict(size=8, color="0.2"),
    )

    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0],
        water_surface.y[0] + 0.1,
        r"HGL",
        ha="left",
        fontdict=dict(size=10, color="navy"),
    )

    n_eddies = 10
    for x, y, s in zip(
        np.linspace(6, 8, n_eddies),
        np.linspace(-1, 2, n_eddies),
        np.random.random(n_eddies),
    ):
        realistic_water(ax, Point(x + 0.1, y - 0.2), 0.05 * s)

    # EGL
    ax.plot(energy_line.x, energy_line.y, c="mediumseagreen", ls="dashed")
    ax.text(
        energy_line.x[0],
        energy_line.y[0] + 0.1,
        r"EGL",
        ha="left",
        fontdict=dict(size=10, color="mediumseagreen"),
    )
    ax.axhline(energy_line.y[0], c="mediumseagreen", ls="dashed", lw=0.5, alpha=0.5)

    # Sections annotations

    ## Energy loss
    ax.plot(
        [energy_line.x[-2]] * 2,
        [energy_line.y[-1], energy_line.y[0]],
        marker="o",
        ms=4,
        lw=1,
        c="darkslategray",
        ls=":",
    )
    ax.text(
        energy_line.x[-2] + 0.2,
        energy_line.y[2:4].mean(),
        r"$h_L$",
        ha="left",
        va="center",
        fontdict=dict(color="darkslategray", size=12),
    )

    for i, x in enumerate([4, 10], start=2):
        ## Sections
        ax.plot([x] * 2, [-4, 5.5], ls="dotted", lw=1, c="gray")
        ax.text(
            x, 5.6, f"Section\n{i-1}", ha="center", fontdict=dict(size=10, color="gray")
        )

        ## Depth
        ax.plot(
            [x] * 2,
            [bottom.y[i], water_surface.y[i]],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (bottom.y[i] + water_surface.y[i]) / 2,
            rf"$y_{i-1}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=12),
        )

        ## Velocity head
        ax.plot(
            [x] * 2,
            [water_surface.y[i], energy_line.y[i]],
            marker="o",
            ms=4,
            lw=2,
            c="darkslategray",
            ls=":",
        )
        ax.text(
            x + 0.2,
            (water_surface.y[i] + energy_line.y[i]) / 2,
            rf"$\dfrac{{Q^2}}{{2gA^2_{i-1}}}$",
            ha="left",
            va="center",
            fontdict=dict(color="darkslategray", size=10),
        )

    # Flow direction
    ax.text(
        bottom.x.max() - 2,
        0,
        r"$Q$",
        ha="right",
        va="center",
        size=12,
        bbox=dict(boxstyle="rarrow,pad=0.3", fc="cornflowerblue", alpha=0.5, lw=0),
    )

    # Final touches for all axes
    ax.set_xlim(bottom.x[0], bottom.x[-1])
    ax.set_ylim(-2.5, 5.6)
    ax.set_aspect("equal")
    # ax.grid(True, color="lightgray")
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig


def FGV_intuition(
    S0: float,
    Se: float,
    Fr: float,
):
    fig, ax = plt.subplots()

    x = np.array([-10, 10])

    bottom = Side(x=x, y=S0 * (x - x.mean()))

    energy = Side(x=x, y=8 + Se * (x - x.mean()))

    Sw = (Se - S0) / (1 - Fr**2)

    water = Side(x=x, y=4 + Sw * (x - x.mean()) + bottom.y)

    # Datum
    ax.axhline(-3, lw=1, color="k", ls="dashed", zorder=0, alpha=0.5)
    ax.text(bottom.x[-1], -3 + 0.1, r"Datum", ha="right", fontdict=dict(size=8))

    ## Bottom
    ax.plot(
        bottom.x,
        bottom.y,
        c="0.50",
        lw=1.5,
        path_effects=[
            pe.withTickedStroke(offset=(0, 0), angle=-45, spacing=6, length=1.3)
        ],
        label="Channel bottom\n" + rf"$S_0 = {S0:+.2f}$",
    )

    ## EGL
    ax.plot(
        energy.x,
        energy.y,
        c="mediumseagreen",
        ls="dashed",
        label="EGL\n" + rf"$Se = {Se:.2f}$",
    )

    ## Water
    ax.plot(water.x, water.y, lw=3, c="navy", label="HGL\n" + rf"$dy/dx = {Sw:+.2f}$")

    # Final touches for all axes
    ax.legend(ncols=3, loc="upper center")
    ax.set_xlim(bottom.x[0], bottom.x[-1])
    ax.set_ylim(-3.1, 12)
    ax.set_aspect("equal")
    # ax.grid(True, color="lightgray")
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    ## Flow direction
    ax.text(
        bottom.x.mean(),
        np.mean(np.concatenate([bottom.y, water.y])),
        r"$Q$",
        ha="left",
        va="center",
        size=12,
        bbox=dict(boxstyle="rarrow,pad=0.3", fc="cornflowerblue", alpha=0.5, lw=0),
    )
    return fig


if __name__ == "__main__":
    page_week_06()
