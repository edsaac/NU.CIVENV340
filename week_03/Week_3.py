import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import networkx as nx
import json, pickle

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
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ziet9v0c.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "### Select a topic:"
        option = st.radio(
            "Select a topic:",
            [
                "Pipes in series/parallel", 
                "Branched systems",
                "Looped networks", 
                "Newton method", 
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
        Pearson Education Inc., Boston.
        
        *****
        """
        with st.expander("🧷 Recommended exercises:"):
            r"""
            - Series/Parallel:
                - 4.1.6
                - 4.1.15
            - Branched system:
                - 4.3.3
            - Networks: (but using Newton method, a spreadsheet or `scipy.optimize.fsolve`)
                - 4.4.2 
                - 4.4.5
                - 4.4.7
                - 4.4.10
            - Design: 4.7.2
            """
        
        cols = st.columns(2)
        with cols[0]:
            r"""
            [![Github Repo](https://img.shields.io/static/v1?label=&message=Repository&color=black&logo=github)](https://github.com/edsaac/NU.CIVENV340)
            """
        with cols[1]:
            r""" [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""
    
    ####################################################################
        
    if option == "Pipes in series/parallel":
        

        cols = st.columns(2)
        with cols[1]:
            st.pyplot(pipes_in_series())

        with cols[0]:
            r""" ## Pipes in series """
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
        
    elif option == "Looped networks":
        r"""
        ## Looped networks
        """

        cols = st.columns(2)
        with cols[0]: show_loops = st.checkbox("Show loops")
        with cols[1]: show_fluxes = st.checkbox("Show fluxes")
        
        st.pyplot(pipes_network_elements(loops=show_loops, fluxes=show_fluxes))


        r"""
        *****
        ### Kirchhoff's circuit laws
        # """
        
        cols = st.columns([1,1.5])

        with cols[0]:
            r"""
            #### ⚖️ Mass balance
            
            Net dicharge in nodes must be zero 
            
            $$
                \sum_j^{\texttt{Node}}{Q_j} = 0
            $$
            
            For example, the mass balance in junction $j_4$:

            $$
                \sum_{\textsf{Pipe } i}^{\substack{\textsf{Pipes} \\ \textsf{on } j_4 }} {Q_{\textsf{Pipe } i}} = 0
            $$

            $$
                Q_{\texttt{4-5}} + Q_{\texttt{4-2}} + Q_{\texttt{4-7}} + 0.1\,{\rm m^3/s} = 0
            $$
            """

        with cols[1]:
            r"""
            #### ⚡ Energy conservation

            Signed head loss in loops must be zero 

            $$
                \sum_i^{\texttt{Loop}}{h_{L_i}} = 0
            $$

            And the energy balance in circuit $\mathtt{II}$:

            $$
                \sum_{\textsf{Pipe } k}^{\substack{\textsf{Pipes on} \\ \textsf{loop } \mathtt{II} }} {h_{\textsf{Pipe } k}} = h_{\texttt{2-3}} + h_{\texttt{3-5}} + h_{\texttt{5-4}} + h_{\texttt{4-2}} = 0
            $$

            Which can be rewritten in terms of discharge:

            $$
                (KQ^m)_{\texttt{2-3}} + (KQ^m)_{\texttt{3-5}} + (KQ^m)_{\texttt{5-4}} + (KQ^m)_{\texttt{4-2}} = 0
            $$

            """

        write_network_equations()

        r"""
        ****
        ### Euler characteristic for plane graphs:
        """
        with st.expander("🌐 From Wikipedia:"):
            st.components.v1.iframe("https:/en.m.wikipedia.org/wiki/Planar_graph#Euler's_formula", scrolling=True, height=400, width=700)
        r"""
        $$
        \begin{align*}
            \textsf{Nodes} - \textsf{Edges} + \textsf{Loops} + \overbrace{1}^{\substack{\textsf{Outer} \\ \textsf{region}}} &=& 2
            \\ \\
            \textsf{Nodes} - \textsf{Edges} + \textsf{Loops} &=& 1  
        \end{align*}
        $$
        
        
        **Number of equations to solve:**

        - $\textsf{Nodes}$ -- Number of mass balance equations
        - $\textsf{Loops}$ -- Number of energy conservation equations
        - $\textsf{Edges}$ -- Number of unknown discharges to be solved
        
        """


    elif option == "Newton method":

        "## Root finding ft. Newton iteration method"
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/8c/Newton_iteration.svg", width=500)
        st.caption("*Source:* [*wikipedia.org*](https://en.wikipedia.org/wiki/Newton%27s_method)")

        r"""
        For a single variable function like the one from the figure:

        $$
            \begin{align*}
                x_{n+1} = x_{n} - \dfrac{f(x_n)}{f'(x_n)}  & \quad \rightarrow & f'(x_n) \underbrace{\left(x_{n+1} - x_{n}\right)}_{\textsf{Should be zero}} = - f(x_n)
            \end{align*}
        $$

        For multiple dimensions, where $\mathbf{Q}$ is a **vector** representing the discharge and $\mathbf{F}$ is the system of mass and energy balance equations:

        $$
            \begin{align*}
                \mathbf{Q}_{n+1} = \mathbf{Q}_{n} - J^{-1}_{\mathbf{F}(\mathbf{Q}_n)} \mathbf{F}(\mathbf{Q}_n)
                & \quad \rightarrow  & 
                \underbrace{J_{\mathbf{F}(\mathbf{Q}_n)}}_{\textsf{Jacobian}} \overbrace{\left( \mathbf{Q}_{n+1} - \mathbf{Q}_{n} \right)}^{\Delta \mathbf{Q}} =  - \mathbf{F}(\mathbf{Q})
            \end{align*}
        $$

        """
        
        r"""
        ******
        #### What is the *Jacobian* $J$?
        """
        
        with st.expander("🌐 From Wikipedia"):
            st.components.v1.iframe("https://mathworld.wolfram.com/Jacobian.html", width=600, height=500, scrolling=True)

        r"""

        The Jacobian is a matrix of all the first-order partial derivatives of a vector function. 

        $$
            J_{\mathbf{F}(\mathbf{Q})} = 
            \begin{bmatrix}
                \dfrac{\partial F_1}{Q_1} & \dots & \dfrac{\partial F_1}{Q_e} \\
                \vdots & \ddots & \vdots \\
                \dfrac{\partial F_m}{Q_1} & \dots & \dfrac{\partial F_m}{Q_m} \\
            \end{bmatrix}
        $$
        
        For example, the mass balance equation of node $j$ looks like:
        $$
            F_j(\mathbf{Q}) = \sum_{k}{Q_{\texttt{j-k}}}
        $$

        $$
            \dfrac{\partial F_j}{\partial Q_i} = 
            \begin{cases}
                1 &\quad \text{ if pipe } k \text{ is connected to node j}  \\
                0 &\quad \text{otherwise} 
            \end{cases}
        $$

        Similarly, for the energy conservation equation on loop $\texttt{I}$:

        $$
            F_{\mathtt{I}}(\mathbf{Q}) = \sum_k{K_kQ_k^m}
        $$

        $$
            \dfrac{\partial F_{\mathtt{I}}}{\partial Q_i} = 
            \begin{cases}
                mK_kQ_k^{m-1} &\quad \text{ if pipe } k \text{ is part of the loop } \texttt{I}  \\
                0 &\quad \text{otherwise} 
            \end{cases}
        $$
        
        If using Darcy-Weisbach equation to calculate head losses, $m=2$:

        $$
            \dfrac{\partial F_{\mathtt{I}}}{\partial Q_i} = 
            \begin{cases}
                2K_kQ_k &\quad \text{ if pipe } k \text{ is part of the loop } \texttt{I}  \\
                0 &\quad \text{otherwise} 
            \end{cases}
        $$
        """

        r"""
        *****
        #### Sign conventions:

        For mass balances:
        - $Q < 0 \quad \text{if entering the node}$
        - $Q > 0 \quad \text{if exiting the node}$

        For energy conservation eqs:
        - $KQ|Q| < 0 \quad \text{if counter-clockwise}$
        - $KQ|Q| > 0 \quad \text{if clockwise}$

        """

        r"""
        **********

        ### Algorithm

        ##### 1️⃣ Make a diagram & define sign conventions:
        """
        cols = st.columns([1,4,1])
        with cols[1]: 
            show_guess = st.checkbox("Show guess")
            st.pyplot(pipes_network_elements(loops=True, fluxes=True, guess=show_guess), dpi=600)
        
        "##### 2️⃣ Write mass and energy conservation equations:"
        write_network_equations()

        r"""
        &nbsp;

        ##### 3️⃣ Assemble the system of equations:

        $$
            J_{\mathbf{F}(\mathbf{Q}_n)} \Delta \mathbf{Q} =  - \mathbf{F}(\mathbf{Q})
        $$
        """            

        with st.expander("Arranged in matrix form.", expanded=True):
            
            st.warning("Notice that we are dropping the mass balance equation for junction 5.", icon="⚠️")

            r"""
            $$
            \def\arraystretch{1.5}
            \left[
            \begin{array}{c:c:c:c:c:c:c:c:c:c}
                \texttt{1-2} & \texttt{2-3} & \texttt{1-6} & \texttt{2-4} & \texttt{3-5} & \texttt{4-5} & \texttt{4-7} & \texttt{5-8} & \texttt{6-7} & \texttt{7-8} \\
                \hline
                1 & \, & 1 & \, & \, & \, & \, & \, & \, & \,  \\  \hdashline
                -1 & 1 & \, & 1 & \, & \, & \, & \, & \, & \,  \\  \hdashline
                \, & -1 & \, & \, & 1 & \, & \, & \, & \, & \, \\  \hdashline
                \, & \, & \, & -1 & \, & 1 & -1 & \, & \, & \, \\  \hdashline
                \, & \, & -1 & \, & \, & \, & \, & \, & 1 & \, \\  \hdashline
                \, & \, & \, & \, & \, & \, & 1 & \, & -1 & 1  \\  \hdashline
                \, & \, & \, & \, & \, & \, & \, & -1 & \, & -1 \\  \hdashline
                2KQ_\texttt{1-2} & \, & -2KQ_\texttt{1-6} & 2KQ_\texttt{2-4} & \, & \, & -2KQ_\texttt{4-7} & \, & -2KQ_\texttt{6-7} & \, \\ \hdashline
                \, & 2KQ_\texttt{2-3} & \, & -2KQ_\texttt{2-4} & 2KQ_\texttt{3-5} & -2KQ_\texttt{4-5} & \, & \, & \, & \, \\ \hdashline
                \, & \, & \, & \, & \, & 2KQ_\texttt{4-5} & 2KQ_\texttt{4-7} & 2KQ_\texttt{5-8} & \, & -2KQ_\texttt{7-8} \\ 
            \end{array}
            \right]

            \begin{bmatrix}
                \Delta Q \\ \hline Q_\texttt{1-2} \\ Q_\texttt{2-3} \\ Q_\texttt{1-6} \\ Q_\texttt{2-4} \\ Q_\texttt{3-5} \\ Q_\texttt{4-5} \\ Q_\texttt{4-7} \\ Q_\texttt{5-8} \\ Q_\texttt{6-7} \\ Q_\texttt{7-8}
            \end{bmatrix}

            = -

            \begin{bmatrix}
                F(Q) \\ \hline +0.3 \\ 0 \\ -0.05 \\ -0.10 \\ 0 \\ 0 \\ -0.15 \\ 0 \\ 0 \\ 0
            \end{bmatrix}
            $$
            
            &nbsp;
            """
        
        r"""
        ##### 4️⃣ Solve for the discharge correction $\Delta Q$:
        """

        cols = st.columns([1,2])

        with cols[0]: 

            r"""
            $$
                \Delta \mathbf{Q} =  - J_{\mathbf{F}(\mathbf{Q}_n)}^{-1}\mathbf{F}(\mathbf{Q})
            $$
            """

        with cols[1]: 
            st.warning("👈 Directly calculating the inverse of a matrix is **computationally expensive**! There are more efficient ways to solve a system of equations.")
        
        r"""
        &nbsp;

        ##### 5️⃣ Recalculate $\mathbf{Q}$ based on the correction $\Delta\mathbf{Q}$:
    
        $$
            \Delta \mathbf{Q} =  \mathbf{Q}_{n+1} -  \mathbf{Q}_{n} \quad \rightarrow \quad \underbrace{\mathbf{Q}_{n+1}}_{\textsf{New guess}} = \Delta \mathbf{Q} + \mathbf{Q}_{n}
        $$

        ##### ↔️ Check if a better guess is needed for $\mathbf{Q}$:
        """
        cols = st.columns(2)

        with cols[0]:
            r"""
            $$
                \textsf{if: } \quad |\Delta \mathbf{Q}| > \varepsilon
            $$
            🔄 Return to step 4 with the new guess for $\mathbf{Q}$
            """ 
        
        with cols[1]:
            r"""
            $$
                \textsf{if: } \quad |\Delta \mathbf{Q}| < \varepsilon
            $$
            🏁 A solution has been found!
            """            

        r"""
        *****
        ### Other methods
        """

        with st.expander("**Hardy-Cross Method**"):
            url = "https://en.m.wikipedia.org/wiki/Hardy_Cross_method"
            st.components.v1.iframe(url, height=500, width=500, scrolling=True)

        with st.expander("**Linear theory method**"):
            _, col, _ = st.columns([1,3,1])
            with col:
                url = "https://doi.org/10.1061/JYCEAJ.0003348"
                fr"""
                Check:

                Wood, D. J., & Charles, C. O. A. (1972). 
                **Hydraulic Network Analysis Using Linear Theory**. 
                *In Journal of the Hydraulics Division (Vol. 98, Issue 7, pp. 1157–1170).*
                American Society of Civil Engineers (ASCE). DOI:[10.1061/jyceaj.0003348]({url})
                """
        
        "****"
        _, col, _ = st.columns([1,3,1])
        with col:
            url = "https://doi.org/10.1002/9780470225059"
            fr"""
            Also check:

            Swamee, P. K., & Sharma, A. K. (2008). 
            **Design of Water Supply Pipe Networks.**
            *John Wiley & Sons, Inc.* 
            DOI:[10.1002/9780470225059]({url})
            """
    
    elif option == "Branched systems":

        r"""
        ## Branched networks

        Aka *tree networks*, these are systems without loops. 
        """

        st.pyplot(three_reservoirs())

        r"""
        ### Three-reservoir problem

        Determine the flow rates between multiple connected reservoirs. 
        For the problem in the figure, we can write energy balance of each of the pipes

        $$
        \begin{array}{rl}
            H_\texttt{A} =& H_\texttt{J} + h_{f_\texttt{A-J}} \\
            H_\texttt{B} =& H_\texttt{J} + h_{f_\texttt{B-J}} \\
            H_\texttt{J} =& H_\texttt{C} + h_{f_\texttt{J-C}} \\
        \end{array}
        $$

        And at the junction $\texttt{J}$, mass must be conserved

        $$
            \sum{Q} = Q_\texttt{A-J} + Q_\texttt{B-J} - Q_\texttt{J-C} = 0
        $$

        In this case, we obtain four equations to solve for four unknowns: the three flow rates
        and the energy head on the junction. We can rewrite the problem to contain only the 
        discharges as unknowns:

        $$
            \def\arraystretch{1.5}
            \begin{cases}
            \begin{array}{rl}
                h_{f_\texttt{A-J}} + h_{f_\texttt{J-C}} =& H_\texttt{A} - H_\texttt{C} \\
                h_{f_\texttt{B-J}} + h_{f_\texttt{J-C}} =& H_\texttt{B} - H_\texttt{C} \\
                Q_\texttt{A-J} + Q_\texttt{B-J} - Q_\texttt{J-C} =& 0
            \end{array}
            \end{cases}
        $$

        Or,
        
        $$
            \def\arraystretch{1.5}            
            \begin{cases}
            \begin{array}{rl}
                K_\texttt{A-J}(Q_\texttt{A-J})^2 + K_\texttt{J-C}(Q_\texttt{J-C})^2 =& H_\texttt{A} - H_\texttt{C} \\
                K_\texttt{B-J}(Q_\texttt{B-J})^2 + K_\texttt{J-C}(Q_\texttt{J-C})^2 =& H_\texttt{B} - H_\texttt{C} \\
                Q_\texttt{A-J} + Q_\texttt{B-J} - Q_\texttt{J-C} =& 0
            \end{array}            
            \end{cases}
        $$
        ********

        ## Solving example 4.6 with `scipy.root`:
        """
        cols = st.columns(2)

        with cols[0]:

            "### 1️⃣ Pipe characteristics"
            with st.echo():
                pipes = pd.DataFrame({
                    "Pipe" : ["A-J", "B-J", "J-C"],
                    "Length (m)" : [1000.0, 4000.0, 2000.0],
                    "Diameter (m)" : [0.30, 0.50, 0.40],
                    "Roughness (m)" : [0.6e-6]*3,
                    }
                )

            pipes.set_index("Pipe", inplace=True)

            st.dataframe(
                pipes.style.format(
                    {"Roughness (m)" : "{:.2E}"}, 
                    precision=2
                ), 
                use_container_width=True
            )

        with cols[1]:
            "### 1️⃣ Node characteristics"

            with st.echo():
                nodes = pd.DataFrame({
                    "Node" : ["A", "B", "C", "J"],
                    "Elevation" : [120.0, 100.0, 80.0, 40.0],
                    "Pressure head" : ["Atm", "Atm", "Atm", "?"]
                    }
                )
            
            nodes.set_index("Node", inplace=True)

            st.dataframe(nodes.style.format(precision=1), use_container_width=True)

        "### 2️⃣ Define the problem system of equations"
        with st.echo():
            from scipy.optimize import root

            def three_reservoirs_problem(
                    discharge_vector,   # [m³/s]
                    diameter_array,
                    length_array,
                    roughness_array):
                
                error = np.zeros_like(discharge_vector)
                KIN_VISCOSITY = 1.0e-6    # [m²/s]
                
                ## Calculations 
                reynolds_array = 4.0 * np.abs(discharge_vector) / (np.pi * diameter_array * KIN_VISCOSITY)
                rel_rough_array = roughness_array / diameter_array
                f_array = swamme_jain(rel_rough_array, reynolds_array)
                K_array = 0.0826 * f_array * length_array / np.power(diameter_array, 5)
                hf_array = K_array * np.power(discharge_vector, 2)
                
                Q1, Q2, Q3 = discharge_vector
                hf1, hf2, hf3 = hf_array

                ## Balance equations
                error[0] = Q1 + Q2 - Q3
                error[1] = hf1 + hf3 - (120-80)
                error[2] = hf2 + hf3 - (100-80)

                return error
        
        "### 🍠 Find the root "
        
        with st.echo():
            solution = root(
                three_reservoirs_problem,   # Equation to solve
                np.array([1,1,1]),          # Initial guess
                args=(
                    pipes["Diameter (m)"],     
                    pipes["Length (m)"],       
                    pipes["Roughness (m)"],
                ),
            )

        "### 🏁 Print solution"       
        if solution.success:
            st.info(solution.message, icon="😎")
            pipes["Discharge (m³/s)"] = solution.x
        
            st.dataframe(
                pipes.style.format(
                    {"Roughness (m)" : "{:.2E}",
                     "Discharge (m³/s)" : "{:.4f}"
                    }, 
                    precision=2
                ), 
                use_container_width=True
            )

        "*****"
        st.warning("What was the pressure in the junction?")
 
    else: 
        r" ### 🚧 Under construction 🚧"

def three_reservoirs():
    from matplotlib.patches import Rectangle, Circle
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])

    def tank(ax, p:Point, width:float, height:float):
        ax.add_patch(Rectangle(p, width, height, fc="#0000aa10", zorder=0))
        ax.plot(
            [p.x, p.x, p.x + width, p.x + width],
            [p.y + 1.1*height, p.y, p.y, p.y + 1.1*height],
            lw=2, c="k", zorder=1)

    fig, ax = plt.subplots()

    # Junction
    junction = Point(8,4)
    ax.add_patch(
        Circle(junction, 0.3, zorder=3),
    )
    ax.text(junction.x + 0.3, junction.y + 0.3, r"$\mathtt{J}$", ha='center')
    
    pjunc = 3.3
    ax.plot([junction.x]*2, [junction.y, junction.y + pjunc])
    ax.text(junction.x, junction.y + pjunc + 0.1, r"$H_\mathtt{J}$", ha='center', color='tab:blue', va='bottom')
    ax.axhline(junction.y + pjunc, xmin=0.4, xmax=0.7, lw=1, color='tab:blue', ls="dashed", zorder=0)

    # Tanks
    tank(ax, tankxy:= Point(0,8), w:=2, h:=1.5)
    ax.text(tankxy.x + w/2, tankxy.y + h, r"$H_\mathtt{A}$", ha='center')
    ax.plot(
        [tankxy.x + w, junction.x], [tankxy.y, junction.y],
        c="k", lw=2)

    tank(ax, tankxy:= Point(4,9), w:=2, h:=2)
    ax.text(tankxy.x + w/2, tankxy.y + h, r"$H_\mathtt{B}$", ha='center')
    ax.plot(
        [tankxy.x + w/2, junction.x], [tankxy.y, junction.y],
        c="k", lw=2)

    tank(ax, tankxy:= Point(10,2), w:=4, h:=1.5)
    ax.text(tankxy.x + w/2, tankxy.y + h, r"$H_\mathtt{C}$", ha='center')
    ax.plot(
        [tankxy.x, junction.x], [tankxy.y, junction.y],
        c="k", lw=2)

    # Datum
    ax.axhline(0.1, xmin=0.5, lw=1, color='k', ls="dashed", zorder=0)
    ax.text(12.2, 0.3, r"Datum", ha="left", fontdict=dict(size=8))

    # Final touches
    #ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    #ax.set_xlim(-2.5, 13.5)
    #ax.set_ylim(-6, 6.0)
    ax.set_aspect('equal')
    #ax.grid(True)
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig

@st.cache_data
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

@st.cache_data
def pipes_network_elements(loops, fluxes, guess=False):
    
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
    if loops:

        loop_arrow_kwargs = dict(connectionstyle="arc3,rad=-0.7", arrowstyle="Simple, tail_width=0.5, head_width=6, head_length=6")

        ax.text(150,125, r"$ \mathtt{I}$", fontdict=dict(size=14), ha="center", va="center")
        ax.add_artist( FancyArrowPatch((120,140), (180,140), **loop_arrow_kwargs) )

        ax.text(475, 187, r"$ \mathtt{II}$", fontdict=dict(size=14), ha="center", va="center")
        ax.add_artist( FancyArrowPatch((435,190), (515,190), **loop_arrow_kwargs) )

        ax.text(475, 62, r"$ \mathtt{III}$", fontdict=dict(size=14), ha="center", va="center")
        ax.add_artist( FancyArrowPatch((435,70), (515,70), **loop_arrow_kwargs) )
    
    # Annotations
    ## Annotate junction
    ax.annotate("Junction (Node)", 
        xy=(310,260), xytext=(350,320), 
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="angle3,angleA=0,angleB=90"
        )
    )

    ## Annotate pipe
    ax.annotate("Pipe (Edge)", 
        xy=(400,0), xytext=(450,-70), 
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="angle3,angleA=10,angleB=-90"
        )
    )

    if fluxes:
        ## Water inputs/outputs
        qin_arrowprops_kwargs = dict(
            edgecolor="blue",
            arrowstyle="->",
            connectionstyle="arc3,rad=0"
            )
        
        qout_arrowprops_kwargs = dict(
            edgecolor="blue",
            arrowstyle="<-",
            connectionstyle="arc3,rad=0"
            )

        q_annotate_kwargs = dict(ha="right", color="blue", size=8)

        ax.annotate(r"$Q = 300 \, {\rm LPS}$ ", 
            xy=(-15,265), xytext=(-10,300), 
            arrowprops=qin_arrowprops_kwargs, **q_annotate_kwargs
        )

        ax.annotate(r"$Q = 100 \, {\rm LPS}$ ", 
            xy=(280,115), xytext=(300-15,80), 
            arrowprops=qout_arrowprops_kwargs, **q_annotate_kwargs
        )

        ax.annotate(r"$Q = 50 \, {\rm LPS}$ ", 
            xy=(660,265), xytext=(740,315), 
            arrowprops=qout_arrowprops_kwargs, **q_annotate_kwargs
        )

        ax.annotate(r"$Q = 150 \, {\rm LPS}$ ", 
            xy=(660,-20), xytext=(750,-70), annotation_clip=False,
            arrowprops=qout_arrowprops_kwargs, **q_annotate_kwargs
        )
    
    if guess:
        guess_kwargs = dict(color="cornflowerblue")
        ax.text(150, 255, r"$200 \rightarrow$", va="bottom", ha="center", **guess_kwargs)
        ax.text(475, 255, r"$80 \rightarrow$", va="bottom", ha="center", **guess_kwargs)
        ax.text(8  , 125, r"$100 \downarrow$", va="center", ha="left", **guess_kwargs)
        ax.text(308, 190, r"$120 \downarrow$", va="center", ha="left", **guess_kwargs)
        ax.text(308, 62 , r"$0 \uparrow$", va="center", ha="left", **guess_kwargs)
        ax.text(475, 130 , r"$20 \rightarrow$", va="bottom", ha="center", **guess_kwargs)
        ax.text(660, 190 , r"$30 \downarrow$", va="center", ha="left", **guess_kwargs)
        ax.text(150, 8 ,  r"$100 \rightarrow$", va="bottom", ha="center", **guess_kwargs)
        ax.text(475, 8 ,  r"$100 \rightarrow$", va="bottom", ha="center", **guess_kwargs)
        ax.text(660, 62 , r"$50 \downarrow$", va="center", ha="left", **guess_kwargs)

    for spine in ax.spines: ax.spines[spine].set_visible(False)
    return fig

def swamme_jain(relative_roughness:float, reynolds_number:float):
    fcalc = 0.25 / np.power(np.log10(relative_roughness/3.7 + 5.74/np.power(reynolds_number, 0.9)), 2)
    return fcalc

swamme_jain = np.vectorize(swamme_jain)
st.session_state.swamme_jain = swamme_jain

def write_network_equations():
    cols = st.columns([1,1.5])

    with cols[0]:
        with st.expander("**Mass balance equations:**", expanded=True):
            r"""

            | Node | Equation |
            |:--:|:--|
            | $j_1$ | $Q_\texttt{1-2} + Q_\texttt{1-6} - 0.3 = 0 $ |
            | $j_2$ | - $Q_\texttt{1-2} + Q_\texttt{2-3} + Q_\texttt{2-4} = 0 $ |
            | $j_3$ | - $Q_\texttt{2-3} + Q_\texttt{3-5} + 0.05 = 0 $ |
            | $j_4$ | - $Q_\texttt{2-4} + Q_\texttt{4-5} - Q_\texttt{4-7} + 0.1 = 0 $ |
            | $j_5$ | - $Q_\texttt{3-5} - Q_\texttt{4-5} + Q_\texttt{5-8} = 0 $ |
            | $j_6$ | - $Q_\texttt{1-6} + Q_\texttt{6-7} = 0 $ |
            | $j_7$ | - $Q_\texttt{6-7} + Q_\texttt{4-7} + Q_\texttt{7-8} = 0 $ |
            | $j_8$ | - $Q_\texttt{5-8} - Q_\texttt{7-8} + 0.15 = 0 $ |
            
            &nbsp;
            """
    
    with cols[1]:
        with st.expander("**Energy conservation eqs**", expanded=True):
            r"""
            
            | Loop | Equation |
            |:--:|:--|
            | $\mathtt{I}$   | $(KQ^m)_\texttt{1-2} + (KQ^m)_\texttt{2-4} - (KQ^m)_\texttt{4-7} - (KQ^m)_\texttt{6-7} - (KQ^m)_\texttt{1-6} = 0 $ |
            | $\mathtt{II}$  | $(KQ^m)_\texttt{2-3} + (KQ^m)_\texttt{3-5} - (KQ^m)_\texttt{4-5} - (KQ^m)_\texttt{2-4} = 0 $ |
            | $\mathtt{III}$ | $(KQ^m)_\texttt{4-5} + (KQ^m)_\texttt{5-8} - (KQ^m)_\texttt{7-8} + (KQ^m)_\texttt{4-7} = 0 $ |
            
            &nbsp;
            """
    return None

# def build_table(netprops:pd.DataFrame):
#     KQ = netprops["2KQ (s/m²)"].to_numpy(dtype=np.float64)
#     print(KQ[0])
#     matrix = np.array([
#         [1.0, 0.0 , 1.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0],
#         [-1.0 , 1.0 , 0.0 , 1.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0],
#         [0.0 , -1.0 , 0.0 , 0.0 , 1.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0],
#         [0.0 , 0.0  , 0.0 , -1.0, 0.0 , 1.0 , -1.0, 0.0 , 0.0 , 0.0],
#         [0.0 , 0.0  , -1.0 , 0.0, 0.0 , 0.0 , 0.0 , 0.0 , 1.0 , 0.0],
#         [0.0 , 0.0  , 0.0  , 0.0, 0.0 , 0.0 , 1.0 , 0.0 , -1.0 , 1.0] ,
#         [0.0 , 0.0  , 0.0  , 0.0, 0.0 , 0.0 , 0.0 , -1.0 , 0.0 , -1.0],
#         [ KQ[0], 0.0, -KQ[2], KQ[3], 0.0, 0.0, -KQ[6], 0.0, -KQ[8], 0.0],
#         [0.0, KQ[1], 0.0, -KQ[3], KQ[4], -KQ[5], 0.0, 0.0, 0.0, 0.0],
#         [0.0, 0.0, 0.0, 0.0, 0.0, KQ[5], KQ[6], KQ[7], 0.0, -KQ[9]]
#     ], dtype=np.float64)
#     print(matrix.dtype)
#     return matrix

def build_graph(nodes_df, edges_df):
    nodes_xy = { k: [ v['x'], v['y']]  for k,v in nodes_df[["x","y"]].to_dict(orient="index").items() }
    edges_ij = edges_df[["i","j"]].to_numpy()
    
    G = nx.DiGraph()
    G.add_nodes_from(nodes_xy)
    G.add_edges_from(edges_ij)

    fig, ax = plt.subplots()
    nx.draw(G, nodes_xy, ax=ax, with_labels=True, width=3, edge_color="purple", node_color="lightgray", font_weight="bold")
    ax.set_aspect('equal')
    
    return G, fig

st.session_state.build_graph = build_graph

# from dataclasses import dataclass
# @dataclass
# class Pipe():
#     diameter:float          # [m]
#     length:float            # [m]
#     roughness:float         # [m]
#     discharge:float = 1e-3  # [m³/s]

#     def __post_init__(self):
#         KIN_VISCOSITY = 1e-6    # [m²/s]

#         self.rel_rough = self.roughness/self.diameter
#         self.reynolds = (4.0 * self.discharge) / (np.pi * self.diameter * KIN_VISCOSITY)

#         self.f = swamme_jain(self.rel_rough, self.reynolds)
#         self.update_K()

#     def update_K(self):
#         self.K = 0.08263 * self.f * self.length / np.power(self.diameter, 5)


if __name__ == "__main__":
    main()