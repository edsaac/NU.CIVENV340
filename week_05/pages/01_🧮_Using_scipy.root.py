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
        \textsf{Critical depth - Trapezoidal section:} \quad \dfrac{Q^2}{g} = A^2 D_h
    $$

    With, """

    cols = st.columns(2)
    with cols[0]: ## Area equation
        r"""
        $$
            A = (b+my)y
        $$
        """
    with cols[1]: ## Hydraulic depth eq.
        r"""
        $$  
            D_h = \dfrac{(b+my)y}{b + 2my}
        $$
        """

    r"""
    ## 1️⃣ Rearange equation to equal zero

    $$
        \dfrac{Q^2}{g} - A^2 D_h = 0
    $$
    """

    r"""
    ****
    ## 2️⃣ Define a function with the equation
    """
    with st.echo():
        g = 9.81  #- m/s²
        def critical_depth_trapezoid(yc, b, m, Q):
            area = (b + m*yc) * yc
            hyd_depth = area / (b + 2*m*yc)
            return (Q**2)/g - (area**2 * hyd_depth)
            
    r"""
    ****
    ## 3️⃣ Call `scipy.optimize.root`
    """
    
    st.components.v1.iframe("https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy-optimize-root", height=500, width=500, scrolling=True)
    "*****"

    cols = st.columns(2)
    with cols[0]:
        bottom_width = st.slider("Bottom width -- $b$", 0.5, 15.0, 5.0, 0.1, format="%.1f")
        side_slope = st.slider("Side slope -- $m$", 0.0, 10.0, 2.0, 0.1, format="%.1f")
        flow_rate = st.slider("Flow rate -- $Q$", 1.0, 100.0, 20.0, 0.1, format="%.1f")
        method = st.selectbox("Root finding method:", ['hybr', 'lm'] )
        initial_guess = st.number_input(r"Initial guess -- $y_{c, \textsf{ guess}}$", 0.0, 100.0, 1.0)
    
    with cols[1]:
        
        "&nbsp;"
        "&nbsp;"

        with st.echo():
            
            from scipy.optimize import root
            
            y_c = root(
                critical_depth_trapezoid,     
                x0 = initial_guess,
                args = (
                    bottom_width,
                    side_slope,
                    flow_rate
                ),
                method = method
            )
            
    r"""
    ****
    ## 🏁 Print final results
    """
    cols = st.columns(2)

    with cols[0]: 
        st.metric(r"$y_{c, \textsf{ guess}}$", f"{initial_guess:.2f} m")
    
    with cols[1]: 
        if y_c.success:
            st.metric("$y_c$", f"{y_c.x[0]:.2f} m")
        else:
            st.error(r"""
            Something went wrong... 
            try changing the initial guess for $f$ or the root-finding method.
            """, icon="🧪")
                
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

