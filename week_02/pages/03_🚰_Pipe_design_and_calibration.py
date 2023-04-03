import streamlit as st
import numpy as np
import pickle

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
    ## Solving an implicit equation
    
    $$
        \textsf{Energy balance eq:} \quad z_1 + \dfrac{p_1}{\gamma} + \dfrac{V_1^2}{2g} = z_2 + \dfrac{p_2}{\gamma} + \dfrac{V_2^2}{2g} + h_L
    $$

    Use Problem 3.5.11 as an example:
    - $Q = 21.5 \textrm{ cfs}$
    - $L = 2500 \textrm{ ft}$
    - $\Delta z = 0 \textrm{ ft}$
    - PVC pipe: $e = 0.000005 \textrm{ ft}$
    - Maximum pressure drop: $\tfrac{\Delta p}{\gamma} < 40 \textrm{ ft}$
    """

    r"""
    ## 1️⃣ Identify equation to solve

    $$
        h_L < \dfrac{\Delta p}{\gamma}
    $$

    Find $D$ such that,

    $$
        f \dfrac{L}{D} \dfrac{V^2}{2g} = \dfrac{40 \textrm{psi}}{\gamma}
    $$
    """

    r"""
    ****
    ## 2️⃣ Define a function with the equation
    """
    with st.echo():
        def swamme_jain(
            relative_roughness:float, 
            reynolds_number:float
            ):

            fcalc = 0.25 / np.power(np.log10(relative_roughness/3.7 + 5.74/np.power(reynolds_number, 0.9)), 2)
            return fcalc

        def energy_balance(
            diameter:float,         # [ft]
            discharge:float,        # [ft³/s]
            length:float,           # [ft]
            roughness:float,        # [ft]
            pressure_drop:float     # [psi]
            ):
            
            g = 32.2                    # ft/s²
            ν = 1.08e-5                 # ft²/s
            γ = 62.3                    # lb/ft³

            area = np.pi/4.0 * np.power(diameter, 2)
            velocity = discharge/area
            
            rel_rough = roughness/diameter
            reynolds = velocity * diameter / ν
            f = swamme_jain(rel_rough, reynolds)
            
            hL = f * (length/diameter) * np.power(velocity,2)/(2*g)
            
            pressure_drop_head = pressure_drop * (12**2) / γ  # Convert pressure [psi] to head [ft]

            return hL - pressure_drop_head

    r"""
    ****
    ## 3️⃣ Call `scipy.optimize.root`
    """
    
    st.components.v1.iframe(
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy-optimize-root", 
        height=500, width=500, scrolling=True)

    "*****"

    cols = st.columns(2)
    with cols[0]:
        length = st.number_input("Pipe length -- $L$ [ft]", 0.0, 5000.0, 2500.0, 1.0, format="%.0f")
        discharge = st.number_input("Discharge -- $Q$ [ft³/s]", 0.0, 50.0, 21.5, 0.1, format="%.1f",  key="cw_Re")
        roughness = st.number_input("Roughness height -- $e$ [ft]", 1e-5, 0.15, 5e-5, format="%.6f")
        pressure_drop = st.number_input("Pressure drop -- $\Delta p$ [psi]", 0.1, 100.0, 40.0, 0.1, format="%.1f")
        initial_guess = st.number_input("Initial guess for $D$", 0.01, 10.0, 1.0, format="%.2f")
        method = st.selectbox("Root finding method:", ['hybr', 'lm'] )
    with cols[1]:
        
        "&nbsp;"

        with st.echo():
            
            from scipy.optimize import root
            
            diameter_design = root(
                energy_balance,     
                x0 = initial_guess,
                args = (
                    discharge,
                    length,
                    roughness,
                    pressure_drop
                ),
                method = method
            )
            
    r"""
    ****
    ## 🏁 Print final results
    """
    cols = st.columns(2)

    with cols[0]: 
        st.metric("*Initial guess* D", f"{initial_guess:.2f} ft")
    
    with cols[1]: 
        if diameter_design.success:
            st.metric("*Solution*", f"{diameter_design.x[0]:.2f} ft")
        else:
            st.error(r"""
            Something went wrong... 
            try changing the initial guess for $f$ or the root-finding method.
            """, icon="🧪")
    
    r"""    
    ****
    ## 🚰 Pick from a catalogue
    """
    cols = st.columns(2)

    with cols[0]:
        st.image("https://www.commercial-industrial-supply.com/wordpress/wp-content/uploads/2020/11/sch40-pvc-piping-dim-chart.jpg", use_column_width=True)

    with cols[1]:
        st.image("https://www.commercial-industrial-supply.com/wordpress/wp-content/uploads/2020/11/sch80-pvc-piping-dim-chart.jpg", use_column_width=True)

    "Check a [catalogue](https://www.charlottepipe.com/)!"
    html = r"""
    <div>
        <object data="https://www.charlottepipe.com/Documents/PL_Tech_Man/Charlotte_Plastics_Tech_Manual.pdf" type="application/pdf" width="100%" height="800">
        </object>
    </div>
    """
    st.components.v1.html(html, height=800, scrolling=True)

if __name__ == "__main__":
    main()

# "For the network characteristics:"

# original_netprops = pd.read_csv("week_03/networks/fig4.9.props.csv")
# original_netprops["e(m)"] = 0.26e-3
# netprops = st.experimental_data_editor(
#     original_netprops.style.format(
#         {
#             "Q(m³/s)" : "{:.3f}",
#             "L(m)" : "{:.1f}",
#             "e(m)" : "{:.2E}",
#         }, precision=2
#     ), use_container_width=True
# )

# calculate_btn = st.button("Calculate *K*", type="primary", use_container_width=True)
# if "calculate_btn_pressed" not in st.session_state:
#     st.session_state["calculate_btn_pressed"] = False

# # if calculate_btn:

# st.session_state["calculate_btn_pressed"] = True
# netprops["e/D"] = netprops["e(m)"] / netprops["D(m)"]
# netprops["Re"] = (4.0 * netprops["Q(m³/s)"]) / (np.pi * netprops["D(m)"] * 1e-6)
# netprops["f"] = swamme_jain(netprops["e/D"], netprops["Re"])
# netprops["K (s²/m⁵)"] = 0.0826 * netprops["f"] * netprops["L(m)"] / np.power(netprops["D(m)"], 5)
# netprops["2KQ (s/m²)"] = 2 * netprops["K (s²/m⁵)"] * netprops["Q(m³/s)"]

# # if st.session_state.calculate_btn_pressed:
# st.dataframe(
#     netprops.style.format(
#         {
#         "Q(m³/s)" : "{:.3f}",
#         "L(m)" : "{:.1f}",
#         "e(m)" : "{:.2E}",
#         "e/D" : "{:.2E}",
#         "Re" : "{:.0f}",
#         "f" : "{:.4f}", 
#         "2KQ (s/m²)" : "{:.1f}"
#         }, precision=2
#     ), 
# use_container_width=True)

# with st.expander("Math"):
#     jacobian = build_table(netprops)
#     F_q = np.array([0.3, 0, -0.05, -0.10, 0, 0, -0.15, 0, 0, 0])

#     jacobian_ltx = a2l.to_ltx(jacobian, frmt='{:.2f}', print_out=False)
#     F_q_ltx = a2l.to_ltx(np.matrix(F_q).T, frmt='{:.2f}', print_out=False)

#     f"""
#     $$
#         {jacobian_ltx} \Delta Q
#         =
#         {F_q_ltx}

#     """  

#     invjacobian = np.linalg.inv(jacobian)
#     invjacobian_ltx = a2l.to_ltx(invjacobian, frmt='{:.2f}', print_out=False)

#     deltaQ = np.matmul(invjacobian, F_q)
#     deltaQ_ltx = a2l.to_ltx(np.matrix(deltaQ).T, frmt='{:.2f}', print_out=False)

#     rf"""
#     $$
#         \Delta Q
#         =
#         {invjacobian_ltx} 
#         {F_q_ltx}
#         =
#         {deltaQ_ltx}
#     """  

# def my_network(Q):
#     Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10 = Q

#     F1 = 0.30 - Q1 -Q2
#     F2 = Q1 - Q2 - Q4
#     F3 = Q2 - Q5 - 0.05
#     F4 = Q4 - Q6 - Q7 - 0.10
#     F5 = Q5 + Q6 - Q8
#     F6 = Q3 - Q9
#     F7 = Q9 + Q7 - Q10 
#     F8 = Q1

