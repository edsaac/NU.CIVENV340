import streamlit as st
import pandas as pd
import networkx as nx
import json
from streamlit.components.v1 import iframe

from ...common import build_graph

def adjacency_matrix():

    url = "https://mathworld.wolfram.com/AdjacencyMatrix.html"

    st.markdown(
        Rf"""
        ## [:link:]({url}) Adjacency matrix
        &nbsp;
        """
    )

    iframe(url, width=600, height=700, scrolling=True)


    st.markdown(
        """
        ****
        ### Building a network
        &nbsp;
        """
    )

    with open("./book/week_03/networks/figureSJ.json") as f:
        network = json.load(f)
        nodes, edges = network["nodes"], network["edges"]

    with st.form("Network data:"):
        cols = st.columns(2)

        with cols[0]:
            "#### 🔵 Nodes"
            nodes_df = pd.DataFrame(nodes).transpose()[["x", "y"]]
            nodes_df = st.data_editor(
                nodes_df, num_rows="dynamic", use_container_width=True
            )

        with cols[1]:
            "#### 📐 Edges"
            edges_df = pd.DataFrame(edges).transpose()[["i", "j"]]
            edges_df = st.data_editor(
                edges_df, num_rows="dynamic", use_container_width=True
            )

        submit_btn = st.form_submit_button("🧱 Build!", use_container_width=True)

    if "submit_btn_pressed" not in st.session_state:
        st.session_state.submit_btn_pressed = False

    if submit_btn or st.session_state.submit_btn_pressed:
        st.session_state.submit_btn_pressed = True

        G, fig = build_graph(nodes_df, edges_df)
        st.pyplot(fig)

        st.markdown("#### Adjacency matrix")
        adjacency_np = nx.to_numpy_array(G)
        adjacency_np = adjacency_np - adjacency_np.T

        if st.checkbox("Directed graph?"):
            adjacency_df = (
                nx.to_pandas_adjacency(G) - nx.to_pandas_adjacency(G).transpose()
            )
        else:
            adjacency_df = nx.to_pandas_adjacency(nx.to_undirected(G))

        st.dataframe(
            adjacency_df.style.format(precision=0)
            .highlight_between(left=0.9, right=1.1, color="#00ff5550")
            .highlight_between(left=-1.1, right=-0.9, color="#ff00aa50"),
            use_container_width=True,
        )


if __name__ == "__main__":
    adjacency_matrix()
