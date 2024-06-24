import streamlit as st
import numpy as np
from streamlit.components.v1 import iframe


def pipe_design_and_calibration():
    st.markdown(
        R"""
        ## Solving an implicit equation
        
        $$
            \textsf{Energy balance eq:} \quad z_1 + \dfrac{p_1}{\gamma} + \dfrac{V_1^2}{2g} = z_2 + \dfrac{p_2}{\gamma} + \dfrac{V_2^2}{2g} + h_L
        $$

        Use Problem 3.5.11 as an example:
        
        |Parameter| Condition|
        |:--------|--------:|
        |Discharge| $Q = 21.5 \textrm{ cfs}$ |
        |Pipe length| $L = 2500 \textrm{ ft}$ |
        |Elevation change| $\Delta z = 0 \textrm{ ft}$ |
        |Material: PVC | $e = 0.000005 \textrm{ ft}$ |
        |Maximum pressure drop | $\Delta p < 40 \textrm{ psi}$ |

        ## 1️⃣ Identify equation to solve

        $$
            h_L < \dfrac{\Delta p}{\gamma}
        $$

        Which, in terms of head, 

        $$
            h_L < 92.3 \textrm{ ft}
        $$

        Find $D$ such that,

        $$
            f \dfrac{L}{D} \dfrac{V^2}{2g} = 92.3 \textrm{ ft}
        $$

        ****
        ## 2️⃣ Define a function with the equation
        """
    )

    with st.echo():

        def swamme_jain(relative_roughness: float, reynolds_number: float):
            fcalc = 0.25 / np.power(
                np.log10(
                    relative_roughness / 3.7 + 5.74 / np.power(reynolds_number, 0.9)
                ),
                2,
            )
            return fcalc

        def energy_balance(
            diameter: float,  # [ft]
            discharge: float,  # [ft³/s]
            length: float,  # [ft]
            roughness: float,  # [ft]
            pressure_drop: float,  # [psi]
        ):
            # Constants
            g = 32.2  # ft/s²
            ν = 1.08e-5  # ft²/s
            γ = 62.3  # lb/ft³

            # Convert pressure to head
            pressure_drop_head = pressure_drop * (12**2) / γ

            area = np.pi / 4.0 * np.power(diameter, 2)
            velocity = discharge / area

            # Friction factor calculation
            rel_rough = roughness / diameter
            reynolds = velocity * diameter / ν
            f = swamme_jain(rel_rough, reynolds)

            # Energy loss
            hL = f * (length / diameter) * np.power(velocity, 2) / (2 * g)

            return hL - pressure_drop_head

    st.markdown(
        R"""
        ****
        ## 3️⃣ Call `scipy.optimize.root`
        """
    )

    iframe(
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy-optimize-root",
        height=500,
        width=500,
        scrolling=True,
    )

    st.divider()

    cols = st.columns(2)
    with cols[0]:
        length = st.number_input(
            R"Pipe length -- $L$ [ft]", 0.0, 5000.0, 2500.0, 1.0, format="%.0f"
        )

        discharge = st.number_input(
            R"Discharge -- $Q$ [ft³/s]", 0.0, 50.0, 21.5, 0.1, format="%.1f", key="cw_Re"
        )

        roughness = st.number_input(
            R"Roughness height -- $e$ [ft]", 1e-5, 0.15, 5e-5, format="%.6f"
        )

        pressure_drop = st.number_input(
            R"Pressure drop -- $\Delta p$ [psi]", 0.1, 100.0, 40.0, 0.1, format="%.1f"
        )

        initial_guess = st.number_input(
            R"Initial guess for $D$", 0.01, 10.0, 1.0, format="%.2f"
        )

        method = st.selectbox("Root finding method:", ["hybr", "lm"])

    with cols[1]:
        "&nbsp;"

        with st.echo():
            from scipy.optimize import root

            diameter_design = root(
                energy_balance,
                x0=initial_guess,
                args=(discharge, length, roughness, pressure_drop),
                method=method,
            )

    st.markdown(
        R"""
        ****
        ## 🏁 Print final results
        """
    )

    cols = st.columns(2)

    with cols[0]:
        st.metric(
            "*Initial guess* D", f"{initial_guess:.3f} ft = {initial_guess*12:.2f} in"
        )

    with cols[1]:
        if diameter_design.success:
            st.metric(
                "*Solution*",
                f"{diameter_design.x[0]:.3f} ft = {diameter_design.x[0]*12:.2f} in",
            )

        else:
            st.error(
                R"""
                Something went wrong... 
                try changing the initial guess for $f$ or the root-finding method.
                """,
                icon="🧪",
            )

    st.markdown(
        R"""    
        ****
        ## 🚰 Pick from a catalogue
        """
    )

    st.caption("Source: [:link:](https://www.commercial-industrial-supply.com/)")
    cols = st.columns(2)
    with cols[0]:
        st.image(
            "https://www.commercial-industrial-supply.com/wordpress/wp-content/uploads/2020/11/sch40-pvc-piping-dim-chart.jpg",
            use_column_width=True,
        )

    with cols[1]:
        st.image(
            "https://www.commercial-industrial-supply.com/wordpress/wp-content/uploads/2020/11/sch80-pvc-piping-dim-chart.jpg",
            use_column_width=True,
        )

    # "For example, [charlottepipe.com](https://www.charlottepipe.com/Documents/PL_Tech_Man/Charlotte_Plastics_Tech_Manual.pdf)!"

    # html = r"""
    # <div>
    #     <object data="https://www.charlottepipe.com/Documents/PL_Tech_Man/Charlotte_Plastics_Tech_Manual.pdf" type="application/pdf" width="100%" height="800">
    #     </object>
    # </div>
    # """
    # html(html, height=800, scrolling=True)


if __name__ == "__main__":
    pipe_design_and_calibration()
