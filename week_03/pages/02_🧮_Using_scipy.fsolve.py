import streamlit as st
import numpy as np
import pandas as pd
import json

def main():

    format_dict = {
        "Q_Guess" : "{:.3f}",
        "Q_Solved" : "{:.3f}",
        "e": "{:.2E}",
        "e/D": "{:.2E}",
        "length" : "{:.1f}",
        "diameter" : "{:.3f}",
        "Re" : "{:.0f}",
        "f" : "{:.4f}", 
        "K" : "{:.1f}",
        "2KQ" : "{:.1f}"
    }

    st.set_page_config(layout='wide')

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    ############################
    
    with open("week_03/networks/figureSJ.json") as f:
        network = json.load(f)
        nodes, edges = network["nodes"], network["edges"]
    
    with st.sidebar:
        ν = st.number_input(r"Kinematic viscosity -- $\nu$ [m²/s]", 1e-8, 1e-3, 1e-6, format="%.2e")

    with st.form("Network data:"):
        r"""
        ## 1️⃣ Organize information
        """

        "#### 🔵 Nodes"
        nodes_df = pd.DataFrame(nodes).transpose()
        nodes_df = st.experimental_data_editor(nodes_df, num_rows="fixed", use_container_width=True)

        "#### 📐 Edges"
        edges_df = pd.DataFrame(edges).transpose()
        edges_df["Q_Guess"] = 0.005
        edges_df = st.experimental_data_editor(edges_df, num_rows="fixed", use_container_width=True)
        
        submit_btn = st.form_submit_button("🧱 Build!", use_container_width=True)

    if submit_btn:
        _, fig = st.session_state.build_graph(nodes_df, edges_df)
        

        r"""
        ****
        ## 2️⃣ Make a sketch
        """
        st.pyplot(fig, transparent=True)

        r"""
        ****
        ## 3️⃣ Guess $Q$
        """
        edges_df["Re"] = 4.0 * edges_df["Q_Guess"] / (np.pi * edges_df["diameter"] * ν)
        edges_df["e/D"] = edges_df["e"] / edges_df["diameter"]
        edges_df["f"] = st.session_state.swamme_jain(edges_df["e/D"], edges_df["Re"])
        edges_df["K"] = 0.0826 * edges_df["f"] * edges_df["length"] / np.power(edges_df["diameter"], 5)
        edges_df["2KQ"] = 2.0 * edges_df["K"] * edges_df["Q_Guess"]

        st.dataframe(
            edges_df.style.format(format_dict, precision=2),
            use_container_width=True
        )

        r"""
        ****
        ## 4️⃣ Build the system of equations
        """
        swamme_jain = st.session_state.swamme_jain
        
        with st.echo():
            def system_of_equations(Q, roughness, D, L):
        
                ## Array of equations
                F = np.zeros_like(Q)
                
                ## Mass balances
                F[0] = Q[0] + Q[3] - 0.50    #- Node A
                F[1] = - Q[0] + Q[1] + Q[4]  #- Node B
                F[2] = - Q[4] + Q[5]         #- Node C
                F[3] = - Q[1] - Q[2] + Q[6] + 0.20  #- Node E
                F[4] = - Q[5] - Q[6] + 0.30  #- Node F

                ## Energy conservation
                Reynolds = 4.0 * Q / (np.pi * D * ν)
                rel_rough = roughness / D
                f = swamme_jain(rel_rough, Reynolds)
                K = 0.0826 * f * L / np.power(D, 5)
                KQ = 2.0 * K * Q

                F[5] = KQ[0] + KQ[1] - KQ[2] - KQ[3]  #-Loop I
                F[6] = KQ[4] + KQ[5] - KQ[6] - KQ[1]  #-Loop II

                return F
        
        r"""
        ****
        ## 5️⃣ Call `scipy.optimize.fsolve`
        """

        st.components.v1.iframe("https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html#scipy-optimize-fsolve", height=500, width=500, scrolling=True)

        with st.echo():
            from scipy.optimize import fsolve
            
            solved_Q = fsolve(
                system_of_equations,     
                x0 = edges_df["Q_Guess"],
                args = (
                    edges_df["e"],
                    edges_df["diameter"],
                    edges_df["length"]
                )
            )
        
        solved_edges_df = edges_df[["i", "j", "length", "diameter", "e"]]
        
        solved_edges_df["Q_Solved"] = solved_Q
        solved_edges_df["Re"] = 4.0 * solved_edges_df["Q_Solved"] / (np.pi * solved_edges_df["diameter"] * ν)
        solved_edges_df["e/D"] = solved_edges_df["e"] / solved_edges_df["diameter"]
        solved_edges_df["f"] = st.session_state.swamme_jain(solved_edges_df["e/D"], solved_edges_df["Re"])
        solved_edges_df["K"] = 0.0826 * solved_edges_df["f"] * solved_edges_df["length"] / np.power(solved_edges_df["diameter"], 5)
        solved_edges_df["2KQ"] = 2.0 * solved_edges_df["K"] * solved_edges_df["Q_Solved"]


        r"""
        ****
        ## 🏁 Print final results
        """
        st.dataframe(
            solved_edges_df.style.format(format_dict, precision=2), 
            use_container_width=True
        )


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

