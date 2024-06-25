import streamlit as st

import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urlparse

from typing import Literal

TOC = Literal[
    "Hydraulic efficiency",
    "Non-erodible channels",
    "Unlined channel design",
    "Weirs and flumes",
    "Gaging stations",
    "Dams and culverts",
]

def page_week_07(option: TOC):
    st.title(option.replace("~", ""))

    if option == "Hydraulic efficiency":
        st.markdown(
            R"""
            ## Hydraulic efficiency

            $$
                \textsf{Manning eq.} \quad Q = \dfrac{1}{n} \, A \, R_h^{2/3} \sqrt{S_0}
            $$
            
            For a given Manning coefficient and channel slope, the discharge can be maximized 
            if the hydraulic radius is maximized, which is achieved if the wetter perimeter is mimized.

            $$
                Q = \dfrac{1}{n} \, \underbrace{A \, R_h^{2/3}}_{\substack{\\🆙}} \sqrt{S_0}
            $$

            The product $A R_h^{2/3}$ is the *section factor for uniform-flow*. Discharge is maximized if this
            section factor is maximized.

            |Shape | Hydraulically efficient section|
            |:--------|:-----------|
            |*Circle* | Half-circle |
            |*Trapezoid*| Half-hexagon |
            |*Rectangle* | Half-square |

            &nbsp;

            *****
            ### Maximizing the section factor for uniform flow:

            For a trapezoidal section, the cross-section area and the wetter perimeter are given by:
            $$
                \begin{array}{rl}
                A =& (b + my)y  \\
                \\
                P_w =& b + 2y \sqrt{1 + m^2}
                \end{array}
            $$

            Or, combined,

            $$
                P_w = \dfrac{A}{y} - my + 2y \sqrt{1 + m^2}
            $$

            Considering $A$ and $m$ constant, an expression for $b$ as a function of $y$ can be found such that
            $P_w$ is minimized

            $$
                \begin{array}{rl}
                    \dfrac{dP_w}{dy} =& \dfrac{d}{dy}\left( \dfrac{A}{y} - my + 2y \sqrt{1 + m^2} \right) = 0 \\
                    \\
                    =&  
                    \dfrac{d}{dy}\left( \dfrac{A}{y} \right) - \dfrac{d}{dy}\left(my\right) + \dfrac{d}{dy}\left(2y \sqrt{1 + m^2} \right) \\
                    \\
                    =& - \dfrac{A}{y^2} - m + 2\sqrt{1 + m^2}\\
                    \\
                    =& - \dfrac{(b + my)y}{y^2} - m + 2\sqrt{1 + m^2}\\
                    \\
                    =& - \dfrac{(b + my)}{y} - m + 2\sqrt{1 + m^2}\\
                    \\
                    =& - \dfrac{b}{y} - 2m + 2\sqrt{1 + m^2}\\
                    \end{array}
            $$

            This means that in order to minimize the wetted perimeter, the base width must be
            
            $$
                \boxed{b = 2y\left(- m + \sqrt{1 + m^2} \right)}
            $$

            Thus, the wetted perimeter is

            $$
                \begin{array}{rl}
                P_w =& b + 2y\sqrt{1+m^2} \\
                    \\
                    =& 2y\left(- m + \sqrt{1 + m^2} \right) + 2y\sqrt{1+m^2}\\
                    \\
                    =& -2ym + 2y \sqrt{1 + m^2} + 2y\sqrt{1+m^2}\\
                    \\
                    =& -2ym + 4y \sqrt{1 + m^2}\\
                \end{array}
            $$

            $$
                \boxed{P_w = 2y \left( 2\sqrt{1+m^2} - m \right)}
            $$

            """
        )

        st.pyplot(wetted_perimeter_v_side_slope_plot())

        cont = st.empty()

        with st.expander("➗ Doing math with sympy:"):
            with st.echo():
                import sympy as sp

                # Define side slope and depth representations
                m, y = sp.symbols("m y")

                # Wetted perimeter
                P_w = 2 * y * (2 * sp.root(1 + m**2, 2) - m)

                # Derivative of wetted perimeter by side slope
                dPdm = sp.diff(P_w, m)

                # Make derivate equal to zero
                eq = sp.Equality(dPdm, 0)

                # Solve for m
                m_optimal = sp.solve(eq, m)

        with cont.container():
            st.markdown(
                Rf"""
                The most efficient section is that for which $m$ minimizes $P_w$,

                $$
                    \begin{{array}}{{rl}}
                    \dfrac{{dP_w}}{{dm}} =& 0 \\
                    \\
                    =& \dfrac{{d}}{{dm}} \left( {sp.latex(P_w)} \right) = 0 \\
                    \\
                    =& {sp.latex(dPdm)} = 0 
                    \end{{array}}
                $$

                The value of $m$ that satisfies this expression is:

                $$
                m = {sp.latex(m_optimal[0])}
                $$
                """
            )

    elif option == "Non-erodible channels":
        st.markdown("## Non-erodible channels (rigid boundary)")

        cols = st.columns(3)

        with cols[0]:
            url = "https://upload.wikimedia.org/wikipedia/commons/2/2f/Trapezoidal_artificial_water_channel.png"
            source = "https://commons.wikimedia.org/wiki/File:Trapezoidal_artificial_water_channel.png"
            st.image(url, use_column_width=True)
            st.caption(
                f"Trapezoidal section <br> Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )

        with cols[1]:
            url = "https://upload.wikimedia.org/wikipedia/commons/8/81/V-Section_artificial_water_channel_02.png"
            source = "https://commons.wikimedia.org/wiki/File:V-Section_artificial_water_channel_02.png"
            st.image(url, use_column_width=True)
            st.caption(
                f"Triangular section <br> Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )

        with cols[2]:
            url = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Semi-circular_artificial_water_channel.png"
            source = "https://commons.wikimedia.org/wiki/File:Semi-circular_artificial_water_channel.png"
            st.image(url, use_column_width=True)
            st.caption(
                f"Circular section <br> Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )

        st.markdown(
            R""" 
            Factors to consider:
            
            |Factor | Description|
            |:--------|:-----------|
            |**Efficiency**     | Geometric conditions that minimize the wetter perimeter |
            |**Cost**| Minimize construction costs |
            |**Practicability** | Available space for construction |
            |**Minimum permissible velocity** | Lowest velocity that will not result in sedimentation or induce vegetation growth |
            |**Freeboard** | Vertical distance between the water surface and the top of the channel |
            
            &nbsp;

            ******
            ### Optimal hydraulic section
            
            For a trapezoidal section, the wetted perimeter is minimized when:

            $$
                b = 2y \left( \sqrt{1+m^2} - m \right)
            $$

            That means that the cross-sectional area and wetted perimeter can be rewritten in terms of only $y$:
            
            $$
                A = (b + my)y = \left( 2y \left( \sqrt{1+m^2} - m \right) + my \right)y
            $$

            $$
                P_w = b + 2y\sqrt{1+m^2} = 2y \left( 2\sqrt{1+m^2} - m \right)
            $$

            Now, the Manning equation can be used to find a solution of the water depth $y$ that satisfies 
            the discharge $Q$ and logitudinal slope $S_0$ conditions.

            $$
                Q = \dfrac{1}{n}\dfrac{A^{5/3}}{P_w^{2/3}} \, \sqrt{S_0}
            $$

            Having found a value for $y$, we can calculate $b$ amd add a freeboard to finalize the design. 

            *****
            ### Solving Example 6.12 with `scipy.root`
            
            |Condition|Notes|
            |:--------|:----|
            |$Q = 15 \textrm{ m³/s}$| Design discharge |
            |$S_0 = 0.00095 $| Longitudinal slope |
            |$m = 2.0 $| Side slope |
            |$n = 0.013$| Concrete |

            &nbsp;
            """
        )

        cols = st.columns([2, 1])

        with cols[1]:
            discharge = st.number_input(
                "Discharge $Q$ [m³/s]", 0.0, 100.0, 15.0, 0.1, format="%.1f"
            )
            n_manning = st.number_input(
                "Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.013, 0.001, format="%.3f"
            )
            long_slope = st.number_input(
                "Bottom slope -- $S_0$ [-]",
                0.00001,
                0.10000,
                0.00095,
                0.0001,
                format="%.5f",
            )
            side_slope = st.number_input(
                "Side slope -- $m$ [-]", 0.0, 10.0, 2.0, 0.1, format="%.1f"
            )
            initial_guess = st.number_input(
                "Initial guess for $y$", 0.01, 50.0, 1.0, format="%.2f"
            )
            method = st.selectbox("Root finding method:", ["hybr", "lm"])

        with cols[0]:
            with st.echo():
                from scipy.optimize import root

                def optimal_trapz_section_error(
                    y: float,  # Depth [m]
                    Q: float,  # Discharge [m³/s]
                    n: float,  # Mannint coefficient [-]
                    S0: float,  # Long. slope [-]
                    m: float,  # Side slope [-]
                ):
                    ## Geometry of a hydraulically optimal section
                    auxm = np.sqrt(1 + m**2)
                    A = (2 * y * (auxm - m) + m * y) * y
                    Pw = 2 * y * (2 * auxm - m)

                    ## Manning equation
                    Qcalc = (
                        1.0 / n * np.power(A, 5 / 3) / np.power(Pw, 2 / 3) * np.sqrt(S0)
                    )

                    error = Q - Qcalc
                    return error

                y_calc = root(
                    optimal_trapz_section_error,
                    initial_guess,
                    args=(
                        discharge,
                        n_manning,
                        long_slope,
                        side_slope,
                    ),
                )

        st.markdown("****** \n\n### 🧩 Solution:")

        if y_calc.success:
            cols = st.columns(4)
            y = y_calc.x[0]
            b = 2 * y * (np.sqrt(side_slope**2 + 1) - side_slope)
            A = (
                2 * y * (np.sqrt(side_slope**2 + 1) - side_slope) + side_slope * y
            ) * y
            P_w = 2 * y * (2 * np.sqrt(1 + side_slope**2) - side_slope)

            with cols[0]:
                st.metric("$\; y$", f"{y:.2f} m")
            with cols[1]:
                st.metric("$\; b$", f"{b:.2f} m")
            with cols[2]:
                st.metric("$\; A$", f"{A:.2f} m²")
            with cols[3]:
                st.metric("$\; P_w$", f"{P_w:.2f} m")

            g = 9.81
            V = discharge / A
            T = b + 2 * y * side_slope
            Dh = A / T
            Fr = V / np.sqrt(g * Dh)

            with cols[0]:
                st.metric("$\; V$", f"{V:.2f} m/s")
            with cols[1]:
                st.metric("$\; T$", f"{T:.2f} m")
            with cols[2]:
                st.metric("$\; D_h$", f"{Dh:.2f} m")
            with cols[3]:
                st.metric("$\; F_r$", f"{Fr:.2f}")

            st.warning("Don't forget to add a freeboard!")

        else:
            st.error(
                R"""
                Something went wrong... 
                try changing the initial guess for $y$ or the root-finding method.
                """,
                icon="🧪",
            )

    elif option == "Unlined channel design":
        st.header("Unlined channels")
        st.markdown(
            R"""
            The principal consideration is that the channel is not eroded under the design
            flow conditions. 
            """
        )

        url = "https://upload.wikimedia.org/wikipedia/commons/d/da/Water_Capture_Channel_-_geograph.org.uk_-_3833453.jpg"
        source = "https://commons.wikimedia.org/wiki/File:Water_Capture_Channel_-_geograph.org.uk_-_3833453.jpg"
        st.image(url, use_column_width=True)
        st.caption(
            f"Unlined channel <br> Source: [{urlparse(source).hostname}]({source})",
            unsafe_allow_html=True,
        )

        st.divider()

        cols = st.columns([1.5, 1])

        with cols[0]:
            st.markdown(
                R"""
                ### 🏎️ Maximum permissible velocity

                1. Select material
                    1. Roughness: $n$
                    2. Stable side slopes: $m$
                    3. Maximum velocity: $V_{\rm max}$
                2. Calculate the hydraulic radius from the Manning equation
                    $$
                        R_h = \left( \dfrac{n \, V_{\rm max}}{\sqrt{S_0}} \right)^{3/2}
                    $$
                3. Given a discharge, calculate the cross-sectional area
                    $$
                        A = \dfrac{Q}{V_{\rm max}}
                    $$
                4. Calculate the wetted perimeter
                    $$
                        P_w = \dfrac{A}{R_h}
                    $$
                5. This way, we obtain a system of two equations to solve for two unknowns, $y$ and $b$
                6. Adjust dimensions and add a freeboard

                """
            )

        with cols[1]:
            url = "https://www.publications.usace.army.mil/LinkClick.aspx?fileticket=4uPtDjMGu64%3d&tabid=16439&portalid=76&mid=43544"
            st.caption(
                f"**Suggested maximum permissible mean channel velocities** <br> Source: U.S. Army Corps of Engineers <br> *Hydraulic Design of Flood Control Channels*, <br> [Enginnering Manual EM 1110-2-1601]({url})",
                unsafe_allow_html=True,
            )
            st.image(
                "./book/assets/img/SuggestedMaxPermissibleMeanChannelVel.png",
                use_column_width=True,
            )

        st.markdown(
            R"""
            *****
            ### Solving Example 6.11 with `scipy.root`
            
            Terrain: *stiff clay*

            |Condition|Notes|
            |--------:|:----|
            |$Q = 9.0 \textrm{ m³/s}$| Design discharge |
            |$S_0 = 0.00280 $| Longitudinal slope |
            |$m = 1.0 $| Side slope |
            |$n = 0.022$| Clean and smooth soil|
            |$V_{\rm max} = 6 \, {\rm ft/s} = 1.83 \, {\rm m/s}$| Recommended value for clay |

            
            &nbsp;
            """
        )

        cols = st.columns([2, 1])

        with cols[1]:
            discharge = st.number_input(
                "Discharge $Q$ [m³/s]", 0.0, 100.0, 9.0, 0.1, format="%.1f"
            )
            n_manning = st.number_input(
                "Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.022, 0.001, format="%.3f"
            )
            long_slope = st.number_input(
                "Bottom slope -- $S_0$ [-]",
                0.00001,
                0.10000,
                0.0028,
                0.0001,
                format="%.5f",
            )
            side_slope = st.number_input(
                "Side slope -- $m$ [-]", 0.0, 10.0, 1.0, 0.1, format="%.1f"
            )
            permissible_vel = st.number_input(
                r"Permissible velocity -- $V_{\rm max}$ [m/s]",
                0.0,
                4.0,
                1.83,
                0.10,
                format="%.2f",
            )

            initial_guess_y = st.number_input(
                "Initial guess for $y$", 0.01, 50.0, 1.0, format="%.2f"
            )
            initial_guess_b = st.number_input(
                "Initial guess for $b$", 0.01, 50.0, 1.0, format="%.2f"
            )

            method = st.selectbox("Root finding method:", ["hybr", "lm"])

        with cols[0]:
            with st.echo():
                from scipy.optimize import root

                def unlined_channel_calculate(
                    GEOMETRY: float,  # [ Depth [m], Base width [m] ]
                    Q: float,  # Discharge [m³/s]
                    Vmax: float,  # Max permissible vel [m/s]
                    n: float,  # Mannint coefficient [-]
                    S0: float,  # Long. slope [-]
                    m: float,  # Side slope [-]
                ):
                    y, b = GEOMETRY

                    ## Manning equation
                    hydr_radius = np.power((n * Vmax) / (np.sqrt(S0)), 3 / 2)

                    ## Required A and Pw
                    required_area = Q / Vmax
                    required_wetted_perimeter = required_area / hydr_radius

                    ## Actual A and Pw from b and y
                    calc_area = (b + m * y) * y
                    calc_wetted_perimeter = b + 2 * y * np.sqrt(1 + m**2)

                    error = [
                        calc_area - required_area,
                        calc_wetted_perimeter - required_wetted_perimeter,
                    ]

                    return error

                geometry_calc = root(
                    unlined_channel_calculate,
                    [initial_guess_y, initial_guess_b],
                    args=(
                        discharge,
                        permissible_vel,
                        n_manning,
                        long_slope,
                        side_slope,
                    ),
                    method=method,
                )

        st.markdown("****** \n\n### 🧩 Solution:")

        if geometry_calc.success:
            st.info(geometry_calc.message, icon="🥳")

            cols = st.columns(4)
            y, b = geometry_calc.x

            A = (b + side_slope * y) * y
            P_w = b + 2 * y * np.sqrt(1 + side_slope**2)

            with cols[0]:
                st.metric("$\; y$", f"{y:.2f} m")
            with cols[1]:
                st.metric("$\; b$", f"{b:.2f} m")
            with cols[2]:
                st.metric("$\; A$", f"{A:.2f} m²")
            with cols[3]:
                st.metric("$\; P_w$", f"{P_w:.2f} m")

            g = 9.81
            Rh = A / P_w
            T = b + 2 * y * side_slope
            Dh = A / T
            V = discharge / A
            Fr = V / np.sqrt(g * Dh)

            with cols[0]:
                st.metric("$\; R_h$", f"{Rh:.2f} m")
            with cols[1]:
                st.metric("$\; T$", f"{T:.2f} m")
            with cols[2]:
                st.metric("$\; D_h$", f"{Dh:.2f} m")
            with cols[3]:
                st.metric("$\; F_r$", f"{Fr:.2f}")

            st.warning("Don't forget to add a freeboard!")

        else:
            st.error(
                R"""
                Something went wrong... 
                try changing the initial guess for $y$ or the root-finding method.
                """,
                icon="🧪",
            )

        st.markdown(    
            R"""
            ******
            ### Tractive force
            
            The base criterion is that the shear force exerted by the flow does not exceed the permissible tractive
            force $\tau_p$ of the channel material. 

            $$
                \textsf{No erosion if:} \quad \tau_b = \gamma R_h S_0 < \tau_p
            $$

            """
        )


    elif option == "Weirs and flumes":
        st.markdown(
            R"""
            ## Weirs

            ### Sharp-crested weir

            In general,

            $$
                {\substack{\textsf{Uncontracted} \\ \textsf{horizontal weir}}}: \quad Q = CLH^{3/2}
            $$

            |Parameter|Description|Units|
            |--------:|:----|:----:|
            |$ Q $| Discharge | Volume/Time |
            |$ C $| Discharge coefficient | Length$^{0.5}$/Time |
            |$ L $| Length of the weir crest| Length |

            &nbsp;

            """
        )

        url = "https://upload.wikimedia.org/wikipedia/commons/3/3e/Floodgate_drum.JPG"
        source = "https://es.wikipedia.org/wiki/Vertedero_hidr%C3%A1ulico#/media/Archivo:Floodgate_drum.JPG"
        st.caption(
            f"Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True
        )
        st.image(url, use_column_width=True)

        # url = "https://upload.wikimedia.org/wikipedia/commons/5/55/Dreieckswehr02.jpeg"
        # source = "https://fr.wikipedia.org/wiki/Seuil_(barrage)#/media/Fichier:Dreieckswehr02.jpeg"
        # st.caption(f"Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True)
        # st.image(url, use_column_width=True)

        url = "https://instrumentationtools.com/wp-content/uploads/2018/01/Weirs-and-flumes-flow-measurement.jpg?ezimgfmt=ng:webp/ngcb2"
        source = "https://instrumentationtools.com/weirs-and-flumes/"
        st.caption(
            f"Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True
        )
        st.image(url, use_column_width=True)

        st.markdown(
            R"""
            Some important types and equations:
            
            |USBR type|Equation|Notes|
            |--------:|:----|:----:|
            |**Standard contracted horizontal**| $$ Q = C(L - 0.2H)H^{3/2} $$ | $$ C = \begin{cases} 3.33 \quad \textsf{(BG)} \\ 1.84 \quad \textsf{(SI)} \end{cases}$$ |
            |**Standard 90° V-notch**| $$ Q = CH^{2.48} $$ | $$ C = \begin{cases} 2.49 \quad \textsf{(BG)} \\ 1.34 \quad \textsf{(SI)} \end{cases}$$ |
            |**Standard trapezoidal** (Cipolletti) | $$ Q = CLH^{3/2} $$ | $$ C = \begin{cases} 3.36 \quad \textsf{(BG)} \\ 1.858 \quad \textsf{(SI)} \end{cases}$$ |
            

            *****
            ### Broad-crested weir

            It's an elevated obstruction that allows critical flow to develop. It can be analyzed as a balance
            of momentum:

            $$
                \overbrace{\rho q \left( \dfrac{q}{y_2} - \dfrac{q}{y_1} \right)}^\textsf{Momentum flux}
                = 
                \dfrac{\gamma}{2} 
                \left( 
                    \underbrace{y_1^2 }_{\substack{\textsf{Upstream} \\ \textsf{pressure}}}
                    - 
                    \underbrace{y_2^2 }_{\substack{\textsf{Downstream} \\ \textsf{pressure}}}
                    - 
                    \underbrace{h(2y_1 - h)}_{\substack{\textsf{Obstruction} \\ \textsf{force}}}
                \right)
            $$

            &nbsp;

            | Parameter | Description   | Units  |
            |:---------:|:--------:|:------------------:|
            |$ q = Q/b $  | Discharge per unit width  | Volume/Time/Length |
            |$ y_1 $  | Upstream depth  | Length |
            |$ y_2 $  | Downstream depth (over the weir)  | Length | 
            |$ h $  | Weir height  | Length | 

            &nbsp;

            """
        )

        url = "https://wiki.tuflow.com/w/thumb.php?f=Broad-crested_weir.jpg&width=640"
        source = "https://wiki.tuflow.com/index.php?title=File:Broad-crested_weir.jpg"
        st.caption(
            f"Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True
        )
        st.image(url, use_column_width=True)

        st.divider()

        _, col, _ = st.columns([1, 3, 1])
        with col:
            url = "https://usbr.gov/tsc/techreferences/mands/wmm/index.htm"
            st.markdown(
                rf"""
                Also check:

                ⏺ U.S. Bureau of Reclamation (2001). <br>
                **Water Measurement Manual: A water resources technical publication**. <br>
                *U.S. Department of the Interior.* <br>
                Website: [usbr.gov]({url})
                
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            R"""
            *****

            ## Critical flow flume

            ### Parshall flume
            """
        )

        url = "https://upload.wikimedia.org/wikipedia/commons/d/d8/Parshall_Flume.svg"
        source = "https://en.wikipedia.org/wiki/Parshall_flume#/media/File:Parshall_Flume.svg"
        st.image(url, use_column_width=True)
        st.caption(
            f"Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True
        )

        st.latex(R"Q = CH_a^n")

        cols = st.columns(2)
        with cols[0]:
            st.markdown(
                R"""

                | Parameter | Description   | Units  |
                |:---------:|:--------:|:------------------:|
                |$ Q $  | Discharge | $\mathrm{ft^3/s}$ |
                |$ H_a $  | Measuring head  | $\mathrm{ft}$ |
                |$ C $  | Empirical coefficient for Parshall flume | 🤔 |
                |$ n $  | Empirical exponent for Parshall flume  | - |

                """
            )

        st.markdown("&nbsp;")

        with cols[1]:
            with st.expander("📋 Coefficients and exponents for Parshall flume"):
                url = "https://usbr.gov/tsc/techreferences/mands/wmm/index.htm"
                source = url
                st.caption(
                    f"Source: [{urlparse(source).hostname}]({source})",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    R"""
                    | Throat width ($W$) | Coefficient ($C$) | Exponent ($n$) |
                    | :----------: | :---------------: | :------------: |
                    | 1 in         | 0.338             | 1.55           |
                    | 2 in         | 0.676             | 1.55           |
                    | 3 in         | 0.992             | 1.55           |
                    | 6 in         | 2.06              | 1.58           |
                    | 9 in         | 3.07              | 1.53           |
                    | 1 ft         | 3.95              | 1.55           |
                    | 2 ft         | 8.00              | 1.55           |
                    | 3 ft         | 12.00             | 1.57           |
                    | 4 ft         | 16.00             | 1.58           |
                    | 5 ft         | 20.00             | 1.59           |
                    | 6 ft         | 24.00             | 1.59           |
                    | 7 ft         | 28.00             | 1.60           |
                    | 8 ft         | 32.00             | 1.61           |
                    | 10 ft        | 39.38             | 1.60           |
                    | 12 ft        | 46.75             | 1.60           |
                    | 15 ft        | 57.81             | 1.60           |
                    | 20 ft        | 76.25             | 1.60           |
                    | 25 ft        | 94.69             | 1.60           |
                    | 30 ft        | 113.13            | 1.60           |
                    | 40 ft        | 150.00            | 1.60           |
                    | 50 ft        | 186.88            | 1.60           |        
                    """
                )

        cols = st.columns(2)

        with cols[0]:
            # with st.expander("📏 Parshall flume dimensions"):
            url = "https://usbr.gov/tsc/techreferences/mands/wmm/fig/F08_09AL.GIF"
            source = "https://usbr.gov/tsc/techreferences/mands/wmm/index.htm"
            st.caption(
                f"Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with cols[1]:
            url = "https://instrumentationtools.com/wp-content/uploads/2018/01/Parshall-flume-measuring-flow.jpg?ezimgfmt=ng:webp/ngcb2"
            source = "https://instrumentationtools.com/weirs-and-flumes/"
            st.caption(
                f"Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        st.markdown("&nbsp;")

        cols = st.columns(2)

        with cols[0]:
            st.markdown(
                R"""
                Depending on the flume width and the ratio $H_b/H_a$, a Parshall flume is either
                operating under **submerged or free flow conditions**
                """
            )

        with cols[1]:
            with st.expander("📋 Threshold for submergence"):
                url = "https://usbr.gov/tsc/techreferences/mands/wmm/index.htm"
                source = url
                st.caption(
                    f"Source: [{urlparse(source).hostname}]({source})",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    R"""
                    |Flume width|Submerged if|
                    |-----:|:-----|
                    |1, 2 or 3in| $\cfrac{H_b}{H_a} > 0.50 $ |
                    |6 or 9in| $\cfrac{H_b}{H_a} > 0.60 $ | 
                    |1ft to 8ft| $\cfrac{H_b}{H_a} > 0.70 $ | 
                    |10ft to 50ft| $\cfrac{H_b}{H_a} > 0.80 $|
                    """
                )

        st.divider()
        _, col, _ = st.columns([1, 3, 1])
        with col:
            url = "https://usbr.gov/tsc/techreferences/mands/wmm/index.htm"
            st.markdown(
                rf"""
                Also check:

                ⏺ U.S. Bureau of Reclamation (2001). <br>
                **Water Measurement Manual: A water resources technical publication**. <br>
                *U.S. Department of the Interior.* <br>
                Website: [usbr.gov]({url})
                
                """,
                unsafe_allow_html=True,
            )

    elif option == "Gaging stations":
        url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/S_Fk_SpreadQm_2.jpg"
        source = "https://www.usgs.gov/media/images/streamflow-measurement-s-fk-spread-creek-wy-13012475"
        st.caption(
            f"**Streamflow measurement in S Fk Spread Creek, WY (13012475)**<br>Source: [{urlparse(source).hostname}]({source})",
            unsafe_allow_html=True,
        )
        st.image(url, use_column_width=True)
        
        url = "https://waterdata.usgs.gov/monitoring-location/04079000/#parameterCode=00065&period=P30D"
        st.link_button("📡 Check the USGS **Waterdata portal**", url=url, use_container_width=True, type="primary")

        st.markdown(
            R"""
            #### Converting stage into discharge:
                        
            $$
                \textsf{Stage-discharge relation} \quad Q = C \, y^n
            $$

            | Parameter | Description   | Units  |
            |:---------:|:--------:|:------------------:|
            |$ Q $  | Discharge | Volume/Time |
            |$ y $  | Measured stage (depth) | Length |
            |$ C $  | Fitting coefficient | Volume/Time/Length$^n$ |
            |$ n $  | Fitting exponent | - |
            """
        )

        
        url = "https://www.usgs.gov/special-topics/water-science-school/science/how-streamflow-measured#overview"
        st.caption(f"Also check: How Streamflow is Measured at [usgs.gov]({url})")
        cols = st.columns(3)

        with cols[0]:
            st.subheader("1. Measuring stream stage")

            url = "https://thebridge.agu.org/files/2018/05/CurrentRiverMissouri.jpg"
            source = "https://thebridge.agu.org/2018/05/17/streamgages-infrastructure-to-protect-infrastructure/"
            st.caption(
                f"**USGS streamgage on the Current River in Montauk State Park in Missouri**<br>Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with cols[1]:
            st.subheader("2. Measuring discharge")
            
            url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/Lowell_Alvin_ADCP4.JPG"
            source = "https://www.usgs.gov/media/images/measuring-boise-river-streamflow-adcp-1"
            st.caption(
                f"**Acoustic Doppler current profiler (ADCP) to measure streamflow on the Boise River**<br>Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        with cols[2]:
            st.subheader("3. Finding $C$ and $n$")
            
            url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/discharge.jpg"
            source = "https://www.usgs.gov/media/images/usgs-stage-discharge-relation-example"
            st.caption(
                f"**Discharge relation example**<br>Source: [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

            url = "https://ars.els-cdn.com/content/image/3-s2.0-B9780128193426000075-f02-09-9780128193426.jpg"
            source = "https://doi.org/10.1016/B978-0-12-819342-6.00007-5"
            st.caption(
                f"**Discharge relation example**<br>Soulis (2021): [{urlparse(source).hostname}]({source})",
                unsafe_allow_html=True,
            )
            st.image(url, use_column_width=True)

        "******"
        _, col, _ = st.columns([1, 3, 1])
        with col:
            url = "https://pubs.er.usgs.gov/publication/tm3A8"
            st.markdown(
                rf"""
                Also check:

                ⏺ Turnipseed & Sauer (2010). <br>
                **Discharge Measurements at Gaging Stations**. <br>
                *In Techniques and Methods. US Geological Survey.* <br>
                DOI: [10.3133/tm3A8]({url})
                
                """,
                unsafe_allow_html=True,
            )

    elif option == "Dams and culverts":
        st.markdown(
            R"""
            ## Dams & spillways

            ### Elements of a dam
            """
        )
        url = "https://www.fema.gov/sites/default/files/2020-08/fema_911_pocket_safety_guide_dams_impoundments_2016.pdf"
        st.caption(
            "Pocket Safety Guide for Dams and Impoundments (FEMA P-911)<br>"
            + f"Source: [{urlparse(url).hostname}]({url})",
            unsafe_allow_html=True,
        )
        st.image("./book/assets/img/embankment.png", use_column_width=True)

        st.markdown(
            R"""
            &nbsp;

            ### Dam classification

            """
        )

        tabs = st.tabs(["**Gravity**", "**Arch**", "**Embankment**", "**Buttress**"])

        imgs = [
            "https://upload.wikimedia.org/wikipedia/commons/9/94/Dworshak_Dam.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/1f/Presa_de_El_Atazar_-_01.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/1c/Tataragi_Dam10n4272.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/9d/Lake_Tahoe_Dam-10.jpg",
        ]

        captions = [
            "Dworshak Dam (ID, USA)",
            "Presa de El Atazar (Madrid, España)",
            "Kurokawa Dam - 多々良木ダム (Asago, Japan)",
            "Lake Tahow Dam (CA, USA)",
        ]

        for tab, img_url, caption in zip(tabs, imgs, captions):
            with tab:
                st.caption(
                    rf"""
                    **{caption}** <br>
                    Source: [{urlparse(img_url).hostname}]({img_url})
                    """,
                    unsafe_allow_html=True,
                )

                st.image(img_url, use_column_width=True)

        st.markdown(
            R"""
            *******
            ## Stilling basin (outlet erosion control)
            """
        )

        img_url = "https://media.defense.gov/2019/Oct/17/2002196661/780/780/0/190326-A-A1412-007.JPG"
        source = "https://www.spa.usace.army.mil/Media/News-Stories/Article/1991774/john-martin-dams-concrete-stilling-basin-in-excellent-condition-after-first-ins/"
        st.caption(
            rf"""
            **John Martin Dam's concrete stilling basin (Highland, UK)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_column_width=True)

        url = "https://www.youtube.com/watch?v=TuQUf-nieVY"
        st.caption(
            f"**Spillways and outlet works** <br>\n Source: Association of State Dam Safety Officials (ASDSO) [youtube.com/@associationofstatedamsafet8080]({url})",
            unsafe_allow_html=True,
        )
        st.video(url)

        st.markdown(
            R"""
            *******
            ## Culverts

            |Inlet| Outlet| Notes |
            |:----|:------|:------|
            |Submerged|Submerged|Pressurized pipe flow|
            |Submerged|Submerged|Full pipe flow with free-discharge outlet|
            |Submerged|Unsubmerged|Partial full pipe flow|
            |Unsubmerged|Unsubmerged|Open-channel flow|

            &nbsp;

            """
        )
    
        img_url = "https://upload.wikimedia.org/wikipedia/commons/a/ad/Culvert_under_the_A835_-_geograph.org.uk_-_3466116.jpg"
        source = "https://www.geograph.org.uk/photo/3466116"
        st.caption(
            rf"""
            **Culvert under the A835 (Highland, UK)** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_column_width=True)

    else:
        st.error("You should not be here!")


def wetted_perimeter_v_side_slope_plot():
    y = 1
    m = np.linspace(0, 3, 50)

    b = 2 * y * (-m + np.sqrt(1 + np.power(m, 2)))
    # A = (b + m * y) * y
    Pw = b + 2 * y * np.sqrt(1 + m**2)
    # Rh = A / Pw

    fig, ax = plt.subplots()
    ax.plot(m, Pw, c="seagreen", lw=5)
    ax.set_ylabel("Wetted perimeter $\quad \dfrac{P_w}{y}$ [-]", fontdict=dict(size=14))
    ax.set_xlabel("Side slope $\quad m$ [-]", fontdict=dict(size=14))
    ax.set_xlim(0, 3.0)
    ax.set_ylim(bottom=0)

    annot = R"""
    Hydraulically efficient section:
    $\dfrac{b}{y} = 2( -m +\sqrt{1 + m^2} )$
    """
    ax.text(0.95, 0.2, annot, ha="right", va="bottom", transform=ax.transAxes)

    m_optimal = np.sqrt(3) / 3
    ax.axvline(m_optimal, ls=":", c="gray")

    ax.text(
        m_optimal, 0.2, "There is a $m$ value \n that minimizes $P_w$", color="gray"
    )

    return fig


if __name__ == "__page__":
    page_week_07()
