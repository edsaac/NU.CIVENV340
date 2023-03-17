import streamlit as st
import plotly.graph_objects as go
import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
import json 
import networkx as nx


def main():
    st.set_page_config(layout='wide')

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ziet9v0c.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "## Week 3"
        "### Select a topic:"
        option = st.radio("Select a topic:",
            ["Pipes in series/parallel", "Branched systems", "Looped networks", "Newton method"],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
        Pearson Education Inc., Boston.
        """

    ####################################################################
        
    if option == "Pipes in series/parallel":
        
        r""" ## Pipes in series """
            
        st.pyplot(pipes_in_series())

        r"""

        The mass between consecutive pipes must be conserved,
        $$
            Q_1 = Q_2 = \mathellipsis  = Q_n
        $$

        Whereas the head loss adds up
        $$
            h_{L} = h_{L_1} + h_{L_2} + \mathellipsis + h_{L_n}
        $$
        
        """

        r""" 
        ****
        ## Pipes in parallel
        
        The mass between the parallel pipes must be conserved,
        $$
            h_1 = h_2 = \mathellipsis = h_{L_n}
        $$

        Whereas the discharge adds up
        $$
            Q = Q_{1} + Q_{2} + \mathellipsis + Q_{n}
        $$
        
        """

    elif option == "Branched systems":
        r" ### 🚧 Under construction 🚧"
        r"""
        ## Branched networks

        """
        
    elif option == "Looped networks":
        r"""
        ## Looped networks
        """

        st.pyplot(pipes_network())

        r"""

        **Kirchhoff's circuit laws:**

        | Rule | Description | Equation |
        |:----|:------|:----:|
        | Mass balance | Net dicharge in nodes must be zero | $ \sum_j^{\texttt{Node}}{Q_j} = 0$ |
        | Energy conservation | Signed head loss in loops must be zero | $\sum_i^{\texttt{Loop}}{h_{L_i}} = 0$ | 
        
        &nbsp;

        For example, the mass balance in junction $J_4$:

        $$
            \sum_{\textsf{Pipe } i}^{\substack{\textsf{Pipes} \\ \textsf{on } J_4 }} {Q_{\textsf{Pipe } i}} = Q_{\texttt{4-5}} + Q_{\texttt{4-2}} + Q_{\texttt{4-7}} = 0
        $$

        And the energy balance in circuit $\mathtt{II}$:

        $$
            \sum_{\textsf{Pipe } j}^{\substack{\textsf{Pipes on} \\ \textsf{loop } \mathtt{II} }} {h_{\textsf{Pipe } j}} = h_{\texttt{2-3}} + h_{\texttt{3-5}} + h_{\texttt{5-4}} + h_{\texttt{4-2}} = 0
        $$

        Which can be rewritten in terms of discharge:

        $$
            \sum_j^{\substack{\textsf{Pipes} \\ \textsf{on } \mathtt{II} }} {h_j} = (KQ^m)_{\texttt{2-3}} + (KQ^m)_{\texttt{3-5}} + (KQ^m)_{\texttt{5-4}} + (KQ^m)_{\texttt{4-2}} = 0
        $$

        """

        st.info("**Number of equations to solve:** \n\nA network with $N$ nodes and $L$ loops results in a system of ? equations.")

    elif option == "Newton method":
        r" ### 🚧 Under construction 🚧"

        "## Root finding ft. Newton iteration method"
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/8c/Newton_iteration.svg", use_column_width=True)
        st.caption("*Source:* [*wikipedia.org*](https://en.wikipedia.org/wiki/Newton%27s_method)")

        r"""
        For a single variable function like the one from the figure:

        $$
            x_{n+1} = x_{n} - \dfrac{f(x_n)}{f'(x_n)}
        $$

        For multiple dimensions, where $Q$ is a **vector** representing the discharge and $F$ is either a mass or an energy balance equation:

        $$
            Q_{n+1} = Q_{n} - \dfrac{F(Q_n)}{F'(Q_n)}
        $$

        **********

        From the previous example:

        
        """

    else: 
        r" ### 🚧 Under construction 🚧"

def pipes_in_series():

    fig, ax = plt.subplots()
    
    # Draw the pipe
    ax.plot([-0.5, 5.0],  [2,1], lw=15, color='gray', alpha=0.5)
    ax.plot([5.0, 10.50], [1,0], lw=7, color='gray', alpha=0.5)
    ax.plot([-0.5, 10.50], [2,0], lw=0.5, color='gray', ls="dashed")

    ax.text(2.5, 0.5, 'Pipe 1', ha='center', va='bottom', axes=ax, rotation=-6)
    ax.text(7.5, -0.15, 'Pipe 2', ha='center', va='bottom', axes=ax, rotation=-6)

    # HGL
    ## Pipe 1
    ### Pressure head
    ax.plot([0, 0], [2,6], lw=2, marker='o', c='red', label="Pressure head")
    ax.plot([4.8, 4.8], [1,4.5], lw=2, marker='o', c='red')
    #ax.text(0.15, 4, r"$\dfrac{p}{\gamma}$", va="center", fontdict=dict(color='red', size=14))

    ### Velocity head
    ax.plot([0,0], [6,7], lw=2, marker='o', c='purple', label="Velocity head")
    ax.plot([4.8, 4.8], [4.5, 5.5], lw=2, marker='o', c='purple')
    #ax.text(0.15, 6.5, r"$\dfrac{V^2}{2g}$", va="center", fontdict=dict(color='purple', size=14))

    ## Pipe 2
    ### Pressure head
    ax.plot([5.2, 5.2], [1,3.0], lw=2, marker='o', c='red')
    ax.plot([10, 10], [0,1.0], lw=2, marker='o', c='red')

    ### Velocity head
    ax.plot([5.2, 5.2], [3, 5], lw=2, marker='o', c='purple')
    ax.plot([10, 10], [1, 3], lw=2, marker='o', c='purple')

    # Datum
    ax.plot([-0.5, 10.50], [-1,-1], lw=1, color='k', ls="dashed")
    ax.text(5, -0.8, r"Datum", ha="center", fontdict=dict(size=8))

    # Draw the HGL & EGL
    ax.plot([0, 4.8, 5.2, 10], [6, 4.5, 3.0, 1], lw=2, c='k', ls=":", label="HGL")
    ax.plot([0, 4.8, 5.2, 10], [7, 5.5, 5.0, 3], lw=2, c='k', ls="-.", label="EGL")

    ## Head loss
    ax.plot([10,10], [3,7], lw=2, marker='o', c='darkorange')

    ax.text(9.75, 5, r"$h_L$", ha="right", va="center", fontdict=dict(color='darkorange', size=14))
    ax.axhline(y=7, lw=0.5, c='gray', ls='dashed')


    # Final touches
    ax.legend(ncols=2, loc="lower center", bbox_to_anchor=(0.5, 0.9))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1.5, 8.5)
    ax.set_aspect('equal')
    ax.grid(False)
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig

def pipes_network():
    
    G = nx.Graph()

    ## Add nodes
    with open("week_03/networks/figure4.9.json") as f:
        network = json.load(f)
    
    G.add_nodes_from(network["nodes"])
    G.add_edges_from(network["edges"])
    
    fig, ax = plt.subplots()
    nx.draw(G, network["nodes"], ax=ax, with_labels=True, width=3, edge_color="purple", node_color="lightgray", font_weight="bold")
    ax.set_aspect('equal')
    
    ## Loops 
    ax.text(150,125, r"$ \mathtt{I}$", fontdict=dict(size=14), ha="center", va="center")
    ax.text(300+350/2, 1.5*125, r"$ \mathtt{II}$", fontdict=dict(size=14), ha="center", va="center")
    ax.text(300+350/2, 0.5*125, r"$ \mathtt{III}$", fontdict=dict(size=14), ha="center", va="center")

    # Annotations
    ## Annotate junction
    ax.annotate("Junction (Node)", 
        xy=(310,260), xytext=(350,320), 
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="angle3,angleA=0,angleB=90"
        )
    )

    ## Annotate junction
    ax.annotate("Pipe (Edge)", 
        xy=(400,0), xytext=(450,-70), 
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="angle3,angleA=10,angleB=-90"
        )
    )

    for spine in ax.spines: ax.spines[spine].set_visible(False)
    return fig

if __name__ == "__main__":
    main()