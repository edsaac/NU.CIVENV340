import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from typing import Literal

from book.common import axis_format

TOC = Literal[
    "Water properties",
    "Fluid classification",
    "Pressure and head",
    "Mass & energy",
    "Problem types",
]


def page_week_01(
    option: TOC,
):
    st.title(option.replace("~", ""), anchor=False)

    if option == "Water properties":
        water_props_path = "./book/week_01/properties.xlsx"

        tabs = st.tabs(["Density", "Viscosity", "Vapor pressure"])

        with tabs[0]:
            st.markdown(
                R"""
                ### Density $\rho_{(T)}$
                """
            )

            density = pd.read_excel(water_props_path, sheet_name="Density_water")
            density["Density (kg/m3)"] = density["Density (g/cm3)"] * 1.0e3

            fig = go.Figure(
                [
                    go.Scatter(
                        x=density["Temperature (C)"],
                        y=density["Density (kg/m3)"],
                        name="Water density",
                        hovertemplate="T = %{x} °C <br><b>ρ = %{y} kg/m³</b>",
                        line=dict(width=5, color="#018749"),
                    )
                ]
            )

            fig.update_layout(
                title_text="""Standard Density of Water as a Function of Temperature<br><i>Data retrieved from the <a href="https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9982163963102441">CRC Handbook of Chemistry and Physics Online</a></i>""",
                yaxis=dict(title="Density [kg/m³]", **axis_format),
                xaxis=dict(title="Temperature [°C]", **axis_format),
            )

            st.plotly_chart(fig, use_container_width=True)

        with tabs[1]:
            st.markdown(
                R"""
                ### Dynamic viscosity $\mu(T)$

                $$
                    \tau = \mu \dfrac{\partial u}{\partial y} 
                $$
                """
            )

            with st.expander("🖼️ **Viscosity diagram**"):
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/9/93/Laminar_shear.svg",
                    use_container_width=True,
                )
                st.caption("*Source* [🛸](https://en.wikipedia.org/wiki/Viscosity)")

            viscosity = pd.read_excel(water_props_path, sheet_name="Viscosity")
            viscosity["Water viscosity (μ) [SI]"] = (
                viscosity["Water viscosity (μ) [SI]"] * 1e-3
            )  # Convert to N.s/m²
            viscosity["Air viscosity (μ) [SI]"] = (
                viscosity["Air viscosity (μ) [SI]"] * 1e-5
            )  # Convert to N.s/m²

            fig = go.Figure(
                [
                    go.Scatter(
                        x=viscosity["Temp (C)"],
                        y=viscosity["Water viscosity (μ) [SI]"],
                        name="Water",
                        hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
                        line=dict(width=2, color="blue"),
                        marker=dict(size=6),
                    ),
                    go.Scatter(
                        x=viscosity["Temp (C)"],
                        y=viscosity["Air viscosity (μ) [SI]"],
                        name="Air",
                        hovertemplate="T = %{x} °C <br><b>μ = %{y:.2e} N.s/m²</b>",
                        line=dict(width=2, color="red"),
                        marker=dict(size=6),
                    ),
                ]
            )

            fig.update_layout(
                height=700,
                title=dict(
                    text="""Viscosities of water and air<br><i>Data retrieved from Table 1.3 - <i>Class textbook</i>""",
                    font_color="#444",
                ),
                yaxis=dict(title="Viscosity [N.s/m²]", type="log", **axis_format),
                xaxis=dict(title="Temperature [°C]", **axis_format),
                legend=dict(
                    title="Fluid",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top",
                    y=0.96,
                    xanchor="right",
                    x=0.96,
                ),
                hovermode="x",
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(fig, use_container_width=True)

            st.info(
                """
                - What is a `poise`? 
                - Who was JLM Poiseuille? 🇫🇷
                """
            )

            st.divider()

            st.markdown(
                R"""
                ## Kinematic viscosity $\nu_{(T)}$

                $$
                    \nu = \dfrac{\mu}{\rho}
                $$

                """
            )

            viscosity = pd.read_excel(water_props_path, sheet_name="Viscosity")
            viscosity["Kinematic water viscosity (ν) [SI]"] = (
                viscosity["Kinematic water viscosity (ν) [SI]"] * 1e-6
            )  # Convert to N.s/m²
            viscosity["Kinematic air viscosity (ν) [SI]"] = (
                viscosity["Kinematic air viscosity (ν) [SI]"] * 1e-6
            )  # Convert to N.s/m²

            fig = go.Figure(
                [
                    go.Scatter(
                        x=viscosity["Temp (C)"],
                        y=viscosity["Kinematic water viscosity (ν) [SI]"],
                        name="Water",
                        hovertemplate="T = %{x} °C <br><b>ν = %{y:.2e} m²/s</b>",
                        line=dict(width=2, color="blue"),
                        marker=dict(size=6),
                    ),
                    go.Scatter(
                        x=viscosity["Temp (C)"],
                        y=viscosity["Kinematic air viscosity (ν) [SI]"],
                        name="Air",
                        hovertemplate="T = %{x} °C <br><b>ν = %{y:.2e} m²/s</b>",
                        line=dict(width=2, color="red"),
                        marker=dict(size=6),
                    ),
                ]
            )

            fig.update_layout(
                height=700,
                title=dict(
                    text="""Viscosities of water and air<br><i>Data retrieved from Table 1.3 - <i>Class textbook</i>""",
                    font_color="#444",
                ),
                yaxis=dict(title="Kinematic viscosity [m²/s]", **axis_format),
                xaxis=dict(title="Temperature [°C]", **axis_format),
                legend=dict(
                    title="Fluid",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top",
                    y=0.50,
                    xanchor="center",
                    x=0.96,
                ),
                hovermode="x",
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(fig, use_container_width=True)

            st.info(
                """
                - What is a `stokes`? 
                - Who was GG Stoke? 🇬🇧 
                """
            )

        with tabs[2]:
            st.markdown(
                R"""
                ### Vapor pressure
                """
            )

            vapor = pd.read_excel(water_props_path, sheet_name="vapor_pressure")
            vapor["Vapor pressure (mH2O)"] = vapor["Vapor pressure (atm)"] * 10.3326

            units = st.radio("Units", ["(atm)", "(mH2O)"], horizontal=True)

            fig = go.Figure(
                [
                    go.Scatter(
                        x=vapor["Temperature"],
                        y=vapor[f"Vapor pressure {units}"],
                        name="Water",
                        hovertemplate="T = %{x} °C <br><b>p<sub>v</sub> = %{y:.2f}"
                        + f"{units} </b>",
                        line=dict(width=4, color="blue"),
                        marker=dict(size=6),
                    )
                ]
            )

            fig.update_layout(
                height=700,
                title=dict(
                    text="""Vapor pressure of water<br> <i>Data retrieved from the <a href="https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9982163963102441">CRC Handbook of Chemistry and Physics Online</a></i>""",
                    font_color="#444",
                ),
                yaxis=dict(title=f"Vapor pressure {units}", **axis_format),
                xaxis=dict(title="Temperature [°C]", **axis_format),
                legend=dict(
                    title="Fluid",
                    font=dict(size=18),
                    orientation="v",
                    bordercolor="gainsboro",
                    borderwidth=1,
                    yanchor="top",
                    y=0.50,
                    xanchor="center",
                    x=0.96,
                ),
                hovermode="x",
                hoverlabel=dict(font_size=18),
            )

            st.plotly_chart(fig, use_container_width=True)

    elif option == "Fluid classification":
        st.markdown(
            """
            ## Fluids

            ### Compressible | Non-compressible

            Does the fluid density change with changes on pressure?
            """
        )

        with st.expander("🧮 As math:"):
            st.markdown(
                R"""
                $$
                    \textsf{Compressibility}: \quad \beta = \dfrac{1}{\rho} \left(\dfrac{\partial \rho}{\partial p}\right)
                $$
                """
            )

        st.markdown(
            R"""
            ### Newtonian | Non-newtonian

            Does the fluid viscosity change with changes on the shear stress?

            """
        )

        with st.expander("🖼️ **Non-newtonian fluids**"):
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/8/89/Rheology_of_time_independent_fluids.svg",
                use_container_width=True,
            )
            st.caption("*Source* [🛸](https://en.wikipedia.org/wiki/Non-Newtonian_fluid)")

        st.markdown(
            R"""
            *****
            ## Flows

            ### Permanent/Transient

            Does the flow change over time?
            

            ### Uniform/Varied

            Does the flow change over space?

            ### Turbulent/Laminar

            Are viscous stresses dominant over the flow inertia?

            **Reynolds number $R_e$:**
            $$
                R_e = \dfrac{\textrm{Inertial forces}}{\textrm{Viscous forces}} = \dfrac{uL}{\nu}
            $$

            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Characteristic length   | $L$   | Length        | 
            |Characteristic velocity | $u$    | Length/Time  |
            |Kinematic viscosity | $\nu$    | Area/Time  | 

            &nbsp;

            ### Subcritical/supercritical

            Are body forces dominant over the flow inertia?

            **Froude number $F_r$**
            $$
                F_r = \dfrac{\textrm{Inertial forces}}{\textrm{Body forces}} = \dfrac{u}{\sqrt{gL}}
            $$

            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Characteristic length   | $L$   | Length        | 
            |Characteristic velocity | $u$    | Length/Time  |
            |Gravitational acceleration | $g$    | Length/Time²  | 

            """
        )

    elif option == "Pressure and head":
        st.markdown(
            R"""
            #### Absolute and gauge pressure

            $$
                p = p_{\rm abs} - p_{\rm atm}
            $$

            """
        )

        st.image(
            "https://www.engineeringtoolbox.com/docs/documents/587/absolute_gauge_pressure.png",
        )
        st.caption(
            "*Source:* [engineeringtoolbox.com](https://www.engineeringtoolbox.com/docs/documents/587/absolute_gauge_pressure.png)"
        )

        st.markdown(
            R"""
            **Barometric formula**

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
        )

        st.warning("Is this equation **dimensionally homogeneous**?")

        fig = go.Figure(
            [
                go.Scatter(
                    x=(height := np.linspace(0, 4000, 100)),
                    y=10.3 * np.exp(-(9.81 * height * 0.02897) / (288.16 * 8.314)),
                    name="Barometric formula",
                    hovertemplate="z = %{x:.1f} m <br><b>h = %{y:.2f} m H<sub>2</sub>O</b>",
                    line=dict(width=5, color="#018749"),
                )
            ]
        )

        fig.update_layout(
            title_text="""Barometric formula<br><i><a href="https://en.wikipedia.org/wiki/Atmospheric_pressure">Source 📖</a></i>""",
            yaxis=dict(title="Atmospheric pressure [m H<sub>2</sub>O]", **axis_format),
            xaxis=dict(title="Elevation above sea level [m]", **axis_format),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            R"""

            ### Pressure and head

            $$
                h = \dfrac{p}{\gamma} = \dfrac{p}{\rho g}
            $$ 

            *****
            ## Hydrostatic pressure distribution

            $$
                p = \rho g \overbrace{y}^{\textrm{Depth}}
            $$ 

            """
        )

        st.info(
            """
            - What are the center of gravity (CG) and the center of pressure (CP) on a surface?
            """
        )

    elif option == "Mass & energy":
        st.markdown(
            R"""

            #### Flow rate and mean velocity

            $$
                Q = V\,A
            $$

            |Parameter|Description|Units|
            |:---:|:---|---:|
            |$Q$| Discharge (volumetric flow rate) | ${\rm m³/s}$|
            |$V$| Mean velocity | ${\rm m/s}$|
            |$A$| Cross-sectional area | ${\rm m²}$|

            &nbsp;

            #### Reynolds number $R_e$

            $$
                R_e = \dfrac{uL}{\nu} = \underbrace{\dfrac{VD}{\nu}}_{\textsf{For circular pipes}} = \dfrac{4Q}{\pi D \nu}
            $$

            """
        )

        with st.expander("Reynolds experiment"):
            st.video("https://www.youtube.com/watch?v=y0WRJtXvpSo")

        st.markdown(
            R"""
            ******
            #### Mass conservation

            The discharge between two sections in a pipe must be the same

            $$
                Q_1 = Q_2
            $$
            
            #### Energy conservation
            """
        )

        with st.expander(
            "**Energy grade line (EGH)** and **hydraulic grade line (HGL)**",
            expanded=True,
        ):
            st.pyplot(gradelines_sketch())
            st.caption("*Source* [🤙🏻](https://edsaac.github.io)")
            # st.image("https://www.pipeflow.com/public/PipeFlowExpertSoftwareHelp/desktop/PipeFlowExpertUserGuide_files/image371.jpg", use_container_width=True)
            # st.caption("*Source* [🛸](https://www.pipeflow.com/public/PipeFlowExpertSoftwareHelp/desktop/Energy_and_Hydraulic_Grade_Lines.htm)")

        st.markdown(
            R"""
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
            |$V^2/2g$| Velocity head | ${\rm m}$|

            &nbsp;

            For a pipe of uniform size, $V_1 = V_2$

            $$
                h_1 + \dfrac{p_1}{\gamma} = h_2 + \dfrac{p_2}{\gamma} + h_L
            $$

            """
        )

    elif option == "Problem types":
        st.markdown(
            R"""
            $$
                h_1 + \dfrac{p_1}{\gamma} + \dfrac{V_1^2}{2g} = h_2 + \dfrac{p_2}{\gamma} + \dfrac{V_2^2}{2g} + h_L(V,D,L,e)
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$h$| Elevation head | ${\rm m}$|
            |$p/\gamma$| Pressure head | ${\rm m}$|
            |$V^2/2g$| Velocity head | ${\rm m}$|
            |$D$| Pipe diameter | ${\rm m}$|
            |$L$| Pipe length| ${\rm m}$|
            |$e$| Roughness height | ${\rm m}$|

            *****
            """
        )

        cols = st.columns(3)

        with cols[0]:
            st.markdown(
                R"""
                ### Type I:
                Solve for pressure
                $$
                    \dfrac{p_2 - p_1}{\gamma}
                $$
                """
            )

        with cols[1]:
            st.markdown(
                r"""
                ### Type II:
                Solve for discharge
                $$
                    Q, V
                $$
                """
            )

        with cols[2]:
            st.markdown(
                r"""
                ### Type III:
                Solve for diameter
                $$
                    A, D
                $$
                """
            )

    else:
        st.error("You should not be here!")


@st.cache_resource
def gradelines_sketch():
    fig, ax = plt.subplots()

    # Draw the pipe
    ax.plot([-0.5, 10.50], [2, 3], lw=15, color="purple", alpha=0.5)
    ax.plot([-0.5, 10.50], [2, 3], lw=1, color="k", ls="dashed")
    ax.text(5, 2.7, "Pipe", ha="center", va="bottom", axes=ax, rotation=6)

    # SECTION 1

    # Annotate section
    ax.annotate(
        "Section 1",
        xy=(0, 2),
        xytext=(1, 3),
        arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=90"),
    )

    ## Elevation head
    ax.plot([0, 0], [0, 2], lw=2, marker="o", c="dimgray")
    ax.text(0.15, 1, r"$h_1$", va="center", fontdict=dict(color="dimgray", size=14))

    ## Pressure head
    ax.plot([0, 0], [2, 8], lw=2, marker="o", c="red")
    ax.text(
        0.15,
        5,
        r"$\dfrac{p_1}{\gamma}$",
        va="center",
        fontdict=dict(color="red", size=14),
    )

    ## Velocity head
    ax.plot([0, 0], [8, 10], lw=2, marker="o", c="purple")
    ax.text(
        0.15,
        9,
        r"$\dfrac{V_1^2}{2g}$",
        va="center",
        fontdict=dict(color="purple", size=14),
    )

    # SECTION 2

    # Annotate section
    ax.annotate(
        "Section 2",
        xy=(10, 3),
        xytext=(7, 1.8),
        arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=90"),
    )

    ## Elevation head
    ax.plot([10, 10], [0, 3], lw=2, marker="o", c="dimgray")
    ax.text(
        9.75,
        1.2,
        r"$h_2$",
        ha="right",
        va="center",
        fontdict=dict(color="dimgray", size=14),
    )

    ## Pressure head
    ax.plot([10, 10], [3, 6], lw=2, marker="o", c="red")
    ax.text(
        9.75,
        4.5,
        r"$\dfrac{p_2}{\gamma}$",
        ha="right",
        va="center",
        fontdict=dict(color="red", size=14),
    )

    ## Velocity head
    ax.plot([10, 10], [6, 8], lw=2, marker="o", c="purple")
    ax.text(
        9.75,
        7,
        r"$\dfrac{V_2^2}{2g}$",
        ha="right",
        va="center",
        fontdict=dict(color="purple", size=14),
    )

    ## Head loss
    ax.plot([10, 10], [8, 10], lw=2, marker="o", c="darkorange")
    ax.text(
        9.75,
        9,
        r"$h_L$",
        ha="right",
        va="center",
        fontdict=dict(color="darkorange", size=14),
    )
    ax.axhline(y=10, lw=0.5, c="gray", ls="dashed")
    ## LINES

    # Draw the datum
    ax.axhline(y=0, lw=2, c="k")
    ax.text(5, 0.1, r"Datum: $z = 0\,{\rm m}$", ha="center")

    # Draw the HGL
    ax.plot([0, 10], [8, 6], lw=2, c="k", ls=":")
    ax.text(5, 7.2, "HGL", ha="center", rotation=-10, fontdict=dict(size=12))

    # Draw the EGL
    ax.plot([0, 10], [10, 8], lw=2, c="k", ls="-.")
    ax.text(5, 9.2, "EGL", ha="center", rotation=-10, fontdict=dict(size=12))

    # Final touches
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal")
    ax.grid(False)
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig
