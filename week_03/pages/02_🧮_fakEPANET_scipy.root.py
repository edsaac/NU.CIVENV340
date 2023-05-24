import streamlit as st
import numpy as np
import pandas as pd
import json, pickle
import gravis as gv
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import networkx as nx


def main():
    with open("assets/page_config.pkl", "rb") as f:
        st.session_state.page_config = pickle.load(f)

    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    format_dict = {
        "Q_Guess": "{:.3f}",
        "Q_Solved": "{:.3f}",
        "e": "{:.2E}",
        "e/D": "{:.2E}",
        "length": "{:.1f}",
        "diameter": "{:.3f}",
        "Re": "{:.0f}",
        "f": "{:.4f}",
        "K": "{:.1f}",
        "2KQ": "{:.1f}",
    }

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        ν = st.number_input(
            r"Kinematic viscosity -- $\nu$ [m²/s]", 1e-8, 1e-3, 1e-6, format="%.2e"
        )

    ############################

    with open("week_03/networks/SJasgJGF.json") as f:
        gv_network = json.load(f)
        nodes, edges = gv_network["graph"]["nodes"], gv_network["graph"]["edges"]

    for edge in gv_network["graph"]["edges"]:
        l = edge["metadata"]["length"]
        d = edge["metadata"]["diameter"]
        e = edge["metadata"]["roughness"]

    for node in gv_network["graph"]["nodes"].values():
        x = node["metadata"]["x"]
        y = node["metadata"]["y"]
        q = node["metadata"]["demand"]

        node["metadata"][
            "click"
        ] = rf" X = {x:.2f} m<br> Y = {y:2f} m<br> Demand = {q:.2e} m³/s"

    ###################################

    with st.form("Network data:"):
        r"""
        ## 1️⃣ Organize information
        """

        cols = st.columns(2)

        with cols[0]:
            "#### 🔵 Nodes"
            nodes_df = {
                id: {
                    "X": val["metadata"]["x"],
                    "Y": val["metadata"]["y"],
                    "Demand": val["metadata"]["demand"],
                }
                for id, val in nodes.items()
            }

            nodes_df = pd.DataFrame(nodes_df).transpose()
            # st.dataframe(nodes_df, use_container_width=True)
            nodes_df = st.experimental_data_editor(
                nodes_df, num_rows="fixed", use_container_width=True
            )

        with cols[1]:
            "#### 📐 Edges"

            edges_df = {
                id: {
                    "Source": val["source"],
                    "Target": val["target"],
                    "Length": val["metadata"]["length"],
                    "Diameter": val["metadata"]["diameter"],
                    "Roughness": val["metadata"]["roughness"],
                }
                for id, val in enumerate(edges)
            }

            edges_df = pd.DataFrame(edges_df).transpose()
            edges_df["Q_Guess"] = 0.1
            edges_df = st.experimental_data_editor(
                edges_df, num_rows="fixed", use_container_width=True
            )
            # st.dataframe(edges_df, use_container_width=True)
            print(edges_df)

        submit_btn = st.form_submit_button("🧱 Build!", use_container_width=True)

    if submit_btn:
        r"""
        ****
        ## 2️⃣ Make a sketch
        """
        for edge, edge_df in zip(edges, edges_df.itertuples()):
            edge["metadata"]["length"] = edge_df.Length
            edge["metadata"]["diameter"] = edge_df.Diameter
            edge["metadata"]["roughness"] = edge_df.Roughness

            edge["metadata"][
                "click"
            ] = rf" Length = {edge_df.Length:.2f} m<br> Diameter = {edge_df.Diameter:2f} m<br> Roughness = {edge_df.Roughness:.2e} m"
            edge["metadata"][
                "hover"
            ] = f"{edge_df.Index}: {edge_df.Source} -- {edge_df.Target}"

        for node, node_df in zip(nodes.values(), nodes_df.itertuples()):
            node["metadata"]["x"] = node_df.X
            node["metadata"]["y"] = node_df.Y
            node["metadata"]["demand"] = node_df.Demand

            node["metadata"][
                "click"
            ] = rf" X = {node_df.X:.2f} m<br> Y = {node_df.Y:2f} m<br><b> Demand = {node_df.Demand:.1f} m³/s</b>"

        build_graph(gv_network)

        r"""
        ****
        ## 3️⃣ Guess $Q$
        """
        edges_df["Re"] = 4.0 * edges_df["Q_Guess"] / (np.pi * edges_df["Diameter"] * ν)
        edges_df["e/D"] = edges_df["Roughness"] / edges_df["Diameter"]
        edges_df["f"] = swamme_jain(edges_df["e/D"], edges_df["Re"])
        edges_df["K"] = (
            0.0826
            * edges_df["f"]
            * edges_df["Length"]
            / np.power(edges_df["Diameter"], 5)
        )
        edges_df["2KQ"] = 2.0 * edges_df["K"] * edges_df["Q_Guess"]

        st.dataframe(
            edges_df.style.format(format_dict, precision=2), use_container_width=True
        )

        r"""
        ****
        ## 4️⃣ Build the system of equations
        """

        with st.echo():

            def system_of_equations(
                Q,  # Discharge [m]
                diameter_array,  # [m]
                length_array,  # [m]
                roughness_array,  # [m]
                demand_array,  # [m³/s]
            ):
                ## Unpack

                ## Array of equations
                F = np.zeros_like(Q)

                ## Mass balances
                F[0] = Q[0] + Q[3] + demand_array[0]  # - Node A
                F[1] = -Q[0] + Q[1] + Q[4] + demand_array[1]  # - Node B
                F[2] = -Q[4] + Q[5] + demand_array[2]  # - Node C
                F[3] = -Q[1] - Q[2] + Q[6] + demand_array[4]  # - Node E
                F[4] = -Q[5] - Q[6] + demand_array[5]  # - Node F

                ## Energy conservation
                reynolds_array = 4.0 * np.abs(Q) / (np.pi * diameter_array * ν)
                rel_rough_array = roughness_array / diameter_array
                f_array = swamme_jain(rel_rough_array, reynolds_array)
                K_array = 0.0826 * f_array * length_array / np.power(diameter_array, 5)
                hf = K_array * np.abs(Q) * Q

                F[5] = -hf[0] - hf[1] + hf[2] + hf[3]  # - Loop I
                F[6] = -hf[4] - hf[5] + hf[6] + hf[1]  # - Loop II

                return F

        r"""
        ****
        ## 5️⃣ Call [`scipy.optimize.root`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)
        """

        st.components.v1.iframe(
            "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html",
            height=500,
            width=500,
            scrolling=True,
        )

        with st.echo():
            from scipy.optimize import root

            solved_Q = root(
                system_of_equations,
                x0=edges_df["Q_Guess"],
                args=(
                    edges_df["Diameter"],
                    edges_df["Length"],
                    edges_df["Roughness"],
                    nodes_df["Demand"],
                ),
                method="lm",
                # tol = 1e-12
            )

        cols = st.columns(2)

        with cols[0]:
            st.info(solved_Q.message)

        with cols[1]:
            with st.expander("📜 log"):
                st.write(solved_Q)

        if solved_Q.success:
            solved_edges_df = edges_df[
                ["Source", "Target", "Length", "Diameter", "Roughness"]
            ]

            solved_edges_df["Q_Solved"] = solved_Q.x
            solved_edges_df["Re"] = (
                4.0
                * np.abs(solved_edges_df["Q_Solved"])
                / (np.pi * solved_edges_df["Diameter"] * ν)
            )
            solved_edges_df["e/D"] = (
                solved_edges_df["Roughness"] / solved_edges_df["Diameter"]
            )
            solved_edges_df["f"] = swamme_jain(
                solved_edges_df["e/D"], solved_edges_df["Re"]
            )
            solved_edges_df["K"] = (
                0.0826
                * solved_edges_df["f"]
                * solved_edges_df["Length"]
                / np.power(solved_edges_df["Diameter"], 5)
            )
            solved_edges_df["2KQ"] = (
                2.0 * solved_edges_df["K"] * solved_edges_df["Q_Solved"]
            )

            r"""
            ****
            ## 🏁 Print final results
            """
            st.dataframe(
                solved_edges_df.style.format(format_dict, precision=2),
                use_container_width=True,
            )

            for edge, discharge in zip(edges, solved_Q.x):
                edge["metadata"]["discharge"] = discharge
                edge["metadata"]["click"] = (
                    edge["metadata"]["click"]
                    + f"<br><b> Discharge = {discharge:.3f} m³/s</b>"
                )

            build_graph(gv_network)


def swamme_jain(relative_roughness: float, reynolds_number: float):
    fcalc = 0.25 / np.power(
        np.log10(relative_roughness / 3.7 + 5.74 / np.power(reynolds_number, 0.9)), 2
    )
    return fcalc


swamme_jain = np.vectorize(swamme_jain)


def build_graph(gv_network):
    fig_gv = gv.vis(
        gv_network,
        graph_height=400,
        details_height=100,
        show_details=True,
        show_menu=True,
        node_hover_tooltip=True,
        edge_hover_tooltip=True,
        use_node_size_normalization=False,
        node_size_normalization_max=150,
        use_edge_size_normalization=True,
        edge_label_data_source="length",
        edge_size_data_source="discharge",
        edge_curvature=-0.05,
        node_drag_fix=True,
        zoom_factor=0.5,
    )

    with NamedTemporaryFile(suffix=".html", mode="r+") as f:
        fig_gv.export_html(f.name, overwrite=True)
        html_fig = f.read()

    st.components.v1.html(html_fig, height=520, width=700, scrolling=True)

    return None


if __name__ == "__main__":
    main()

# def build_graph(nodes_df, edges_df):
#     nodes_xy = { k: [ v['X'], v['Y']]  for k,v in nodes_df[["X","Y"]].to_dict(orient="index").items() }
#     edges_ij = edges_df[["Source","Target"]].to_numpy()

#     G = nx.DiGraph()
#     G.add_nodes_from(nodes_xy)
#     G.add_edges_from(edges_ij)

#     fig, ax = plt.subplots()
#     nx.draw(G, nodes_xy, ax=ax, with_labels=True, width=3, edge_color="purple", node_color="lightgray", font_weight="bold")
#     ax.set_aspect('equal')

#     return G, fig

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
