import streamlit as st
import pickle
import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urlparse

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets4.lottiefiles.com/private_files/lf30_nep75hmm.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=100)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [   
                "Hydraulic efficiency",
                "Non-erodible channels",
                "Unlined channel design",
                "Flow measurement devices [Pipes]",
                "Flow measurement devices [Channels]"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
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
    if option == "Hydraulic efficiency":
        r"""
        ## Hydraulic efficiency

        $$
            \textsf{Manning eq.} \quad Q = \dfrac{1}{n} A \, \, R_h^{2/3} \sqrt{S_0}
        $$
        
        For a given Manning coefficient and channel slope, the discharge can be maximized 
        if the hydraulic radius is maximized, which is achieved if the wetter perimeter is mimized.

        $$
            Q = \dfrac{1}{n} \underbrace{A \, \, R_h^{2/3}}_{\substack{\\🆙}} \sqrt{S_0}
        $$

        The product $A R_h^{2/3}$ is the *section factor for uniform-flow*. Discharge is maximized if this
        section factor is maximized.

        |Shape | Hydraulically efficient section|
        |:--------|:-----------|
        |*Circle* | Half-circle |
        |*Trapezoid*| Half-hexagon |
        |*Rectangle* | Half-square |

        &nbsp;

        """

        # with st.echo():

        #     import sympy as sp
        #     A, Pw, b, m, y = sp.symbols("A P_w b m y")
            
        #     A = (b + m*y)*y
        #     Pw = b + 2*y*sp.sqrt(1 + m**2)

        #     Rh = A/Pw 
            
        #     difficult = A**sp.Rational(5, 3) / Pw**sp.Rational(2,3)

        #     dAdy = sp.diff(A, y)

        #     difficultdy = sp.diff(difficult, y)

        #     solve = sp.Eq(difficultdy, 0)
            
        r"""
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

        st.pyplot(wetted_perimeter_v_side_slope_plot())

        cont = st.empty()

        with st.expander("➗ Doing math with sympy:"):
            with st.echo():
                import sympy as sp
                
                # Define side slope and depth representations
                m, y = sp.symbols("m y")     

                # Wetted perimeter
                P_w = 2*y*(2*sp.root(1 + m**2, 2) - m )     
                
                # Derivative of wetted perimeter by side slope
                dPdm = sp.diff(P_w, m)                      
                
                # Make derivate equal to zero
                eq = sp.Equality(dPdm, 0)      
                
                # Solve for m
                m_optimal = sp.solve(eq, m)


        with cont.container():
            rf"""
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

    elif option == "Non-erodible channels":
        
        "## Non-erodible channels (rigid boundary)"        
        
        cols = st.columns(3)

        with cols[0]:
            url = "https://upload.wikimedia.org/wikipedia/commons/2/2f/Trapezoidal_artificial_water_channel.png"
            source = "https://commons.wikimedia.org/wiki/File:Trapezoidal_artificial_water_channel.png"
            st.image(url, use_column_width=True)
            st.caption(f"Trapezoidal section <br> Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True)

        with cols[1]:
            url = "https://upload.wikimedia.org/wikipedia/commons/8/81/V-Section_artificial_water_channel_02.png"
            source = "https://commons.wikimedia.org/wiki/File:V-Section_artificial_water_channel_02.png"
            st.image(url, use_column_width=True)
            st.caption(f"Triangular section <br> Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True)

        with cols[2]:
            url = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Semi-circular_artificial_water_channel.png"
            source = "https://commons.wikimedia.org/wiki/File:Semi-circular_artificial_water_channel.png"
            st.image(url, use_column_width=True)
            st.caption(f"Circular section <br> Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True)


        r""" 
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

        cols = st.columns([2,1])

        with cols[1]:
            discharge = st.number_input("Discharge $Q$ [m³/s]", 0.0, 100.0, 15.0, 0.1, format="%.1f")
            n_manning = st.number_input("Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.013, 0.001, format="%.3f")
            long_slope = st.number_input("Bottom slope -- $S_0$ [-]", 0.00001, 0.10000, 0.00095, 0.0001, format="%.5f")
            side_slope = st.number_input("Side slope -- $m$ [-]", 0.0, 10.0, 2.0, 0.1, format="%.1f")
            initial_guess = st.number_input("Initial guess for $y$", 0.01, 50.0, 1.0, format="%.2f")
            method = st.selectbox("Root finding method:", ['hybr', 'lm'] )


        with cols[0]:
            with st.echo():
                from scipy.optimize import root

                def optimal_trapz_section_error(
                    y:float,    # Depth [m]
                    Q:float,    # Discharge [m³/s]
                    n:float,    # Mannint coefficient [-]
                    S0:float,   # Long. slope [-]
                    m:float,    # Side slope [-]
                    ):
                    
                    ## Geometry of a hydraulically optimal section
                    auxm = np.sqrt(1 + m**2)
                    A  = (2*y*(auxm - m) + m*y) * y
                    Pw = 2*y * (2 * auxm - m)

                    ## Manning equation 
                    Qcalc = 1.0/n * np.power(A, 5/3)/np.power(Pw, 2/3) * np.sqrt(S0)
                    
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
                    )
                )

        "****** \n\n### 🧩 Solution:"

        
        if y_calc.success:
            
            cols = st.columns(4)
            y = y_calc.x[0]
            b = 2*y * (np.sqrt(side_slope**2 + 1) - side_slope)
            A = (2*y*(np.sqrt(side_slope**2 + 1) - side_slope) + side_slope*y) * y
            P_w = 2*y * (2 * np.sqrt(1 + side_slope**2) - side_slope)
            
            with cols[0]: st.metric("$\; y$", f"{y:.2f} m")
            with cols[1]: st.metric("$\; b$", f"{b:.2f} m")
            with cols[2]: st.metric("$\; A$", f"{A:.2f} m²")
            with cols[3]: st.metric("$\; P_w$", f"{P_w:.2f} m")

            g = 9.81
            V = discharge/A
            T = b + 2*y*side_slope
            Dh = A/T
            Fr = V/np.sqrt(g*Dh)

            with cols[0]: st.metric("$\; V$", f"{V:.2f} m")
            with cols[1]: st.metric("$\; T$", f"{T:.2f} m")
            with cols[2]: st.metric("$\; D_h$", f"{Dh:.2f} m²")
            with cols[3]: st.metric("$\; F_r$", f"{Fr:.2f} m")

            st.warning("Don't forget to add a freeboard!")

        else:
            st.error(r"""
            Something went wrong... 
            try changing the initial guess for $y$ or the root-finding method.
            """, icon="🧪")
            
            
    elif option == "Unlined channel design":

        "## Unlined channels"
        r"""
        The principal consideration is that the channel is not eroded under the design
        flow conditions. 
        """

        url = "https://upload.wikimedia.org/wikipedia/commons/d/da/Water_Capture_Channel_-_geograph.org.uk_-_3833453.jpg"
        source = "https://commons.wikimedia.org/wiki/File:Water_Capture_Channel_-_geograph.org.uk_-_3833453.jpg"
        st.image(url, use_column_width=True)
        st.caption(f"Unlined channel <br> Source: [{urlparse(source).hostname}]({source})", unsafe_allow_html=True)

        "*****"

        cols = st.columns([1.5,1])

        with cols[0]:
            r"""
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
        
        with cols[1]:
            url = "https://www.publications.usace.army.mil/LinkClick.aspx?fileticket=4uPtDjMGu64%3d&tabid=16439&portalid=76&mid=43544"
            st.caption(f"**Suggested maximum permissible mean channel velocities** <br> Source: U.S. Army Corps of Engineers <br> *Hydraulic Design of Flood Control Channels*, <br> [Enginnering Manual EM 1110-2-1601]({url})", unsafe_allow_html=True)
            st.image("assets/img/SuggestedMaxPermissibleMeanChannelVel.png", use_column_width=True)

        r"""
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

        cols = st.columns([2,1])

        with cols[1]:
            discharge = st.number_input("Discharge $Q$ [m³/s]", 0.0, 100.0, 9.0, 0.1, format="%.1f")
            n_manning = st.number_input("Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.022, 0.001, format="%.3f")
            long_slope = st.number_input("Bottom slope -- $S_0$ [-]", 0.00001, 0.10000, 0.0028, 0.0001, format="%.5f")
            side_slope = st.number_input("Side slope -- $m$ [-]", 0.0, 10.0, 1.0, 0.1, format="%.1f")
            permissible_vel = st.number_input(r"Permissible velocity -- $V_{\rm max}$ [m/s]", 0.0, 4.0, 1.83, 0.10, format="%.2f")
            
            initial_guess_y = st.number_input("Initial guess for $y$", 0.01, 50.0, 1.0, format="%.2f")
            initial_guess_b = st.number_input("Initial guess for $b$", 0.01, 50.0, 1.0, format="%.2f")
            
            method = st.selectbox("Root finding method:", ['hybr', 'lm'] )


        with cols[0]:
            with st.echo():
                from scipy.optimize import root

                def unlined_channel_calculate(
                    GEOMETRY:float,     # [ Depth [m], Base width [m] ]
                    Q:float,            # Discharge [m³/s]
                    Vmax:float,         # Max permissible vel [m/s]
                    n:float,            # Mannint coefficient [-]
                    S0:float,           # Long. slope [-]
                    m:float,            # Side slope [-]
                    ):

                    y,b = GEOMETRY

                    ## Manning equation
                    hydr_radius = np.power((n*Vmax) / (np.sqrt(S0)), 3/2)

                    ## Required A and Pw
                    required_area = Q/Vmax
                    required_wetted_perimeter = required_area/hydr_radius

                    ## Actual A and Pw from b and y
                    calc_area = (b + m*y) * y
                    calc_wetted_perimeter = b + 2*y*np.sqrt(1 + m**2)

                    error = [
                        calc_area - required_area, 
                        calc_wetted_perimeter - required_wetted_perimeter
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
                    method=method
                )

        "****** \n\n### 🧩 Solution:"

        
        if geometry_calc.success:
            
            st.info(geometry_calc.message)

            cols = st.columns(4)
            y, b = geometry_calc.x
            
            A = (b + side_slope*y) * y
            P_w = b + 2*y*np.sqrt(1 + side_slope**2)
            
            with cols[0]: st.metric("$\; y$", f"{y:.2f} m")
            with cols[1]: st.metric("$\; b$", f"{b:.2f} m")
            with cols[2]: st.metric("$\; A$", f"{A:.2f} m²")
            with cols[3]: st.metric("$\; P_w$", f"{P_w:.2f} m")

            g = 9.81 
            Rh = A/P_w
            T = b + 2*y*side_slope
            Dh = A/T
            V = discharge/A
            Fr = V/np.sqrt(g*Dh)

            with cols[0]: st.metric("$\; R_h$", f"{Rh:.2f} m")
            with cols[1]: st.metric("$\; T$", f"{T:.2f} m")
            with cols[2]: st.metric("$\; D_h$", f"{Dh:.2f} m")
            with cols[3]: st.metric("$\; F_r$", f"{Fr:.2f}")

            st.warning("Don't forget to add a freeboard!")

        else:
            st.error(r"""
            Something went wrong... 
            try changing the initial guess for $y$ or the root-finding method.
            """, icon="🧪")

        r"""
        ******
        ### Tractive force
        
        The base criterion is that the shear force exerted by the flow does not exceed the permissible tractive
        force $\tau_p$ of the channel material. 

        $$
            \textsf{No erosion if:} \quad \tau_b = \gamma R_h S_0 < \tau_p
        $$

        """
    elif option=="Flow measurement devices [Pipes]":
        r"""
        ## Pipes
        
        """

    elif option=="Flow measurement devices [Channels]":
        r"""
        ## Channels
        
        """

    else: 
        st.error("You should not be here!")
        

def wetted_perimeter_v_side_slope_plot():
    y = 1
    m = np.linspace(0,3,50)

    b =  2*y * ( -m + np.sqrt(1 + np.power(m,2)) )
    A = (b + m*y)*y
    Pw = b + 2*y*np.sqrt(1 + m**2)
    Rh = A/Pw
    
    fig, ax = plt.subplots()
    ax.plot(m, Pw, c="seagreen", lw=5)
    ax.set_ylabel("Wetted perimeter $\quad \dfrac{P_w}{y}$ [-]", fontdict=dict(size=14))
    ax.set_xlabel("Side slope $\quad m$ [-]", fontdict=dict(size=14))
    ax.set_xlim(0, 3.0)
    ax.set_ylim(bottom=0)
    
    annot = r"""
    Hydraulically efficient section:
    $\dfrac{b}{y} = 2( -m +\sqrt{1 + m^2} )$
    """
    ax.text(
        0.95, 0.2,
        annot, ha="right", va="bottom",
        transform=ax.transAxes)

    m_optimal = np.sqrt(3)/3
    ax.axvline(m_optimal, ls=":", c="gray")
    
    ax.text(
        m_optimal, 0.2,
        "There is a $m$ value \n that minimizes $P_w$",
        color="gray")

    return fig

if __name__ == "__main__":
    main()