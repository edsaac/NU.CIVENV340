import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt

def main():

    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    ############################
    
    r"""
    **Solving an initial value problem (IVP)**
    
    ## 1️⃣ Identify equation and boundary conditions

    $$
        \begin{array}{rl}
        \textsf{Gradually varied flow:} & \dfrac{dy}{dx} = \dfrac{S_e - S_0}{1 - \mathsf{F_r}^2} \\
        \\
        \textsf{Boundary condition:} & y(x_0) = y_0
        \end{array}
    $$

    """

    r"""
    ****
    ## 2️⃣ Calculate normal and critical depths
    
    #### $y_n$
    """
    with st.echo():
        def normal_depth_trapezoidal_section(
                y:float,    # Depth [m]
                S0:float,   # Channel bottom slope [-]
                Q:float,    # Discharge [m³/s]
                b:float,    # Bottom width [m]
                m:float,    # Side slope [-]
                nMan:float  # Manning coefficient [-]
            ):

            A = (b + m*y) * y                   # Area
            Pm = b + 2*y*np.sqrt(1+m**2)        # Wetted perimeter
            Rh = A/Pm                           # Hydraulic radius
            return Q - 1.0/nMan * A * Rh**(2/3) * np.sqrt(S0)

    "#### $y_c$"
    with st.echo():
        def critical_depth_trapezoidal_section(
                y:float,    # Depth [m]
                Q:float,    # Discharge [m³/s]
                b:float,    # Bottom width [m]
                m:float,    # Side slope [-]
            ):
            
            A = (b + m*y) * y                   # Area
            T = b + 2*m*y                       # Top width
            g = 9.81                            # SI Units
            return 1 - (Q**2 * T)/(g * A**3)
    
    r"""
    ****
    ## 3️⃣ Calculate normal and critical depths
    """
    
    cols = st.columns(2)
    with cols[0]:

        width = st.number_input("Width -- $b$ [m]", 0.1, 20.0, 4.0, 1.0, format="%.2f")
        discharge = st.number_input("Discharge -- $Q$ [m³/s]", 0.1, 100.0, 12.5, 1.0, format="%.1f")
        n_manning = st.number_input("Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.025, 0.001, format="%.3f")
        bottom_slope = st.number_input("Bottom slope -- $S_0$ [-]", -0.1000, -0.0001, -0.0010, 0.0001, format="%.4f")
        side_slope = st.number_input("Side slope -- $m$ [-]", 0.0, 10.0, 1.0, 0.1, format="%.4f")
        y0 = st.number_input("Boundary condition -- $y(x_0)$ [m]", 0.01, 10.0, 2.0, 0.1, format="%.2f")
    
    with cols[1]:
        "****"
        lilcols = st.columns(2)
        with lilcols[0]: "##### Normal depth calculation"
        with lilcols[1]: normaldepth_container = st.empty()

        with st.expander("🧮 scipy.optimize.root"):
            with st.echo():
                from scipy.optimize import root
                
                normal_depth = root(
                    normal_depth_trapezoidal_section,     
                    x0 = y0,
                    args = (
                        - bottom_slope,
                        discharge,
                        width,
                        side_slope,
                        n_manning, 
                    ),
                )

        with normaldepth_container.container():
            if normal_depth.success:
                st.metric("$\; y_n$", f"{normal_depth.x[0]:.2f} m")
        
        "*****"
        
        lilcols = st.columns(2)
        with lilcols[0]: "##### Critical depth calculation"
        with lilcols[1]: critdepth_container = st.empty()

        with st.expander("🧮 scipy.optimize.root"):
            with st.echo():
                from scipy.optimize import root
                
                critical_depth = root(
                    critical_depth_trapezoidal_section,     
                    x0 = 0.1,
                    args = (
                        discharge,
                        width,
                        side_slope,
                    ),
                )

        with critdepth_container.container():
            if critical_depth.success:
                st.metric("$\; y_c$", f"{critical_depth.x[0]:.2f} m")

    r"""
    ****
    ## 4️⃣ Define a function with the differential equation
    """
    with st.echo():
        def gvf_trapezoidal_section(
                x:float,    # Longitudinal distance [m]
                y:float,    # Depth [m]
                S0:float,   # Channel bottom slope [-]
                Q:float,    # Discharge [m³/s]
                b:float,    # Bottom width [m]
                m:float,    # Side slope [-]
                nMan:float  # Manning coefficient [-]
            ):

            A = (b + m*y) * y                   # Area
            T = b + 2*m*y                       # Top width
            Pm = b + 2*y*np.sqrt(1+m**2)        # Wetted perimeter
            Rh = A/Pm                           # Hydraulic radius
            g = 9.81                            # SI Units

            Se = ((nMan * Q)/(A * Rh**(2/3)))**2  # Manning eq, slope of EGL
            sqFr = (Q**2 * T)/(g * A**3)          # Froude num squared
            dydx = (Se - S0)/(1 - sqFr)           # GVF equation
            return dydx
    
    r"""
    ****
    ## 5️⃣ Calculate solution with `scipy.solve_ivp`
    """
    
    st.components.v1.iframe("https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html#scipy-integrate-solve-ivp", height=500, width=500, scrolling=True)
    
    "&nbsp;"

    with st.echo():
        
        from scipy.integrate import solve_ivp
        
        water_surface = solve_ivp(
            gvf_trapezoidal_section,  # Equation to solve
            [0, 2000],                 # Interval for solving the equation
            [y0],                     # Boundary (initial) condition
            args = (
                - bottom_slope,
                discharge,
                width,
                side_slope,
                n_manning, 
            ),
            t_eval=np.arange(0, 2000, 1),
            method="RK45"
        )
        
        x = water_surface.t
        y = water_surface.y[0] - x*bottom_slope

    r"""
    ****
    ## 🏁 Print final results
    """
    
    with st.expander("📄 Log:"):
        st.write(water_surface)

    if water_surface.success:
        st.pyplot(plot_water_profile(x,y,normal_depth.x[0], critical_depth.x[0], bottom_slope))

    else:
        st.error(r"""
        Something went wrong... 
        """, icon="🧪")

    _, col, _ = st.columns([1,1.8,1])
    with col: st.info("### 🤔 What type of profile is this?")

def plot_water_profile(
        x,
        y,
        y_n,
        y_c,
        S0
    ):
    
    fig,ax = plt.subplots()
    ax.plot(x,y, lw=3, c="navy", label=r"Water surface: $y(x)$")
    
    ax.axline([0,0], slope=-S0, c="k", label="Bottom elevation")
    ax.axline([0,y_n], slope=-S0, c="green", ls="dashed", label=r"Normal depth: $y_n$")
    ax.axline([0,y_c], slope=-S0, c="red", ls="dotted", label=r"Critical depth: $y_c$")


    # Datum
    ax.axhline(0, lw=1, color='k', ls="dashed", zorder=2)
    ax.text(x.mean(), 0, r"Datum", ha="center", va="bottom", fontdict=dict(size=8))

    # Final touches for all axes
    ax.set_xlabel("Longitudinal distance -- $x$ [m]")
    ax.set_ylabel("Elevation [m]")
    ax.legend(ncols=2, loc="lower center", bbox_to_anchor=[0.5,0.94])
    ax.set_xlim(x.min(), x.max())
    ax.grid(True, color="lightgray")
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    
    #ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.tick_params(labelsize=8, length=2)
    return fig


if __name__ == "__main__":
    main()