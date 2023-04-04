import streamlit as st
import plotly.graph_objects as go
from itertools import cycle
import numpy as np
import pickle

def colebook_white(relative_roughness:float, reynolds_number:float, fguess:float=0.01):   
    fcalc = 1.0 / np.power(- 2.0 * np.log10(relative_roughness/3.7 + 2.51/(reynolds_number*np.sqrt(fguess))), 2)
    return fcalc

def swamme_jain(relative_roughness:float, reynolds_number:float):
    fcalc = 0.25 / np.power(np.log10(relative_roughness/3.7 + 5.74/np.power(reynolds_number, 0.9)), 2)
    return fcalc

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)

    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    axis_format = dict(title_font_size=20,
        tickfont_size=16,
        showline=True,
        color="RGBA(1, 135, 73, 0.3)",
        tickcolor="RGBA(1, 135, 73, 0.3)",
        showgrid=True,
        griddash="dash",
        linewidth=1,
        gridcolor="RGBA(1, 135, 73, 0.3)")

    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_9e8rwhfi.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            ["Friction head loss", "Empirical relationships", "Equations summary", "Accessories", "Momentum and forces"],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
        Pearson Education Inc., Boston.
        
        *****
        """

        with st.expander("🧷 Recommended exercises:"):
            r"""
            - Direct: 3.5.2
            - Direct: 3.5.8
            - Design: 3.5.12
            - Calibration: 3.5.14
            - 3.3.6 + Calculate the K of the elbow.
            """
        
        cols = st.columns(2)
        with cols[0]:
            r"""
            [![Github Repo](https://img.shields.io/static/v1?label=&message=Repository&color=black&logo=github)](https://github.com/edsaac/NU.CIVENV340)
            """
        with cols[1]:
            r""" [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""
    

        "****"

    ####################################################################
        
    if option == "Friction head loss":

        r"""

        $$
            \textsf{Total head loss:} \quad h_L = \underbrace{h_f}_{\substack{\textsf{Due} \\ \textsf{friction}}} + \underbrace{\sum{h_a}}_{\substack{\textsf{Due} \\ \textsf{accesories} }}
        $$

        ## Head loss due friction $h_f$

        **Darcy-Weisbach equation:**
        
        $$
            h_f = f \left( \dfrac{L}{D}\right) \dfrac{V^2}{2g}
        $$

        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$f$| Friction factor | $ - $|
        |$L$| Pipe length | ${\rm m}$ |
        |$D$| Pipe diameter | ${\rm m}$|
        |$V^2/2g$| Velocity head | ${\rm m}$|
        
        &nbsp;
        """

        st.warning("Is Darcy-Weisbach equation dimensionally homogeneous?")

        r"""
        In terms of discharge: 

        $$
        \begin{align*}
            h_f &= f \left( \dfrac{L}{D} \right) \dfrac{8}{\pi^2 D^4 g} \, Q^2 \\
                \\
            h_f &\approx \dfrac{0.08263\,f\,L}{D^5} Q^2 \quad& \textsf{(For SI units)}
        \end{align*}
        $$


        In general:

        $$
            h_f = KQ^m
        $$

        |Parameter|Description|Units|
        |:---:|:---:|:---:|
        |$K$| ⁉️ | ❓ |
        |$m$| ⁉️ | ❓ |

        ****
        ## Friction factor $f$
        """

        tabs = st.tabs(["Laminar flow", "Turbulent flow"])    
        
        with tabs[0]:
            r"""
            **Hagen-Poiseuille law:**
            
            $$
                f = \dfrac{64}{R_e}
            $$

            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$R_e$| Reynolds number | $ - $|
            """
        
        with tabs[1]:
            r"""
            **Colebrook-White equation:**
            
            $$
                \dfrac{1}{\sqrt{f}} = -2\log\left( \dfrac{e}{3.7\,D} + \dfrac{2.51}{R_e \, \sqrt{f}} \right)
            $$
            
            |Parameter|Description|Units|
            |:---:|:---|:---:|
            |$e$| Roughness height | $ {\rm m} $|
            |$e/D$| Relative roughness | $ - $
            |$D$| Pipe diameter | ${\rm m}$|
            |$R_e$| Reynolds number | $ - $|

            &nbsp;
            """

            with st.expander("🧮 How to solve this *implicit* equation?", expanded=False):
                
                cols = st.columns(2)
                with cols[0]:
                    eD = st.number_input("Relative roughness $e/D$", 1e-6, 0.05, 1e-5, format="%.2e", key="cw_eD")
                with cols[1]:
                    Re = st.number_input("Reynolds number $R_e$", 1e3, 1e9, 1e6, format="%.2e",  key="cw_Re")
                
                r"""
                $$
                    f = \left[-2\log\left( \dfrac{e}{3.7\,D} + \dfrac{2.51}{R_e \, \sqrt{f}} \right)\right]^{-2}
                $$"""

                cols = st.columns([1,0.5,1])
                with cols[1]: "# ⬅️"
                with cols[2]:
                    fguess = st.number_input("$f$ guessed", 0.008, 0.1, 0.05, format="%.6f", key="cw_fg")
                with cols[0]: 
                    f = colebook_white(eD, Re, fguess)
                    st.number_input("$f$ calculated", 0.008, 0.1, f, format="%.6f", disabled=True, key="cw_fc")
                    

            r"""
            &nbsp;

            **Swamme-Jain equation:**

            $$
                f = \dfrac{0.25}{\left[ \log{\left( \dfrac{e}{3.7\,D} + \dfrac{5.74}{R_e^{0.9}} \right)} \right]^2}
            $$

            &nbsp;
            """

            with st.expander("🧮 How to solve this equation?"):
                
                cols = st.columns(2)
                with cols[0]:
                    eD = st.number_input("Relative roughness $e/D$", 1e-6, 0.05, 1e-5, format="%.2e", key="sj_eD")
                with cols[1]:
                    Re = st.number_input("Reynolds number $R_e$", 1e3, 1e9, 1e6, format="%.2e", key="sj_Re")
                
                f = swamme_jain(eD, Re)
                st.number_input("$f$ calculated", 0.008, 0.1, f, format="%.6f", disabled=True, key="sj_fc")


            st.warning("How close is the Swamme-Jain equation to the implicit Colebrook-White equation?")

        r"""
        ****
        ## Moody diagram
        """

        st.image("https://upload.wikimedia.org/wikipedia/commons/d/d9/Moody_EN.svg", use_column_width=True)
        st.caption("*Source* [🛸](https://commons.wikimedia.org/wiki/File:Moody_EN.svg)")

        r"""
        ******
        ## Hydraulically smooth and rough pipes
        
        $$
        \begin{align*}
            \textsf{Hydraulically smooth:} &\quad \delta > 1.7\,e \\
            \textsf{Hydraulically rough:}  &\quad \delta < 0.08\,e
        \end{align*}
        $$
        
        """

        cols = st.columns([1,2,1])
        with cols[1]:
            st.image("https://media.springernature.com/full/springer-static/image/chp%3A10.1007%2F978-3-030-34086-5_1/MediaObjects/483272_1_En_1_Fig4_HTML.png?as=webp", use_column_width=True)
            st.caption("*Source* [CS James (2019), Hydraulic Structures. Springer 🛸](https://link.springer.com/chapter/10.1007/978-3-030-34086-5_1)")

        r"""
        |Parameter|Description|Units|Notes|
        |:---:|:---|:---:|:---|
        |$e$| Roughness height | $ {\rm m} $ | Same as $k$ in the image |
        |$\delta$| Thickness of the viscous sublayer | $ {\rm m} $| $\delta =  0.37 \, D \, R_e ^{-1/5} \; \textsf{\dag}$  |
        """
        st.caption("† For turbulent flow in a circular pipe")
        # |$u^*$| Shear velocity | $ {\rm m/s} $| $u^* = \sqrt{\dfrac{\tau_0}{\rho}}$ |
        # |$\tau_0$| Wall shear stress | $ {\rm N/m²} $| $\tau_0 = \mu \dfrac{\partial u}{\partial y}\biggm\vert_{y=0}$ |


        r"""
        ### Velocity profiles & shear stress
        """

        st.image("https://engineeringlibrary.org/static/img/References/DOE-Fundamentals-Handbook/fluid-flow/fig-5-laminar-and-turbulent-flow-velocity-profiles.webp")
        st.caption("*Source:* [https://engineeringlibrary.org 🛸](https://engineeringlibrary.org/reference/laminar-and-turbulent-fluid-flow-doe-handbook)")

        with st.expander("**Hydraulically smooth or rough?**"):
            cols = st.columns(2)
            with cols[0]: 
                r"""
                $$
                    \textsf{Plastic}: \quad e \approx 0.0015 {\rm mm}
                $$
                """            

                st.image("https://images.pexels.com/photos/5752926/pexels-photo-5752926.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", use_column_width=True)
                st.caption(f"*Photo of a man with a cap posing near pipes* [🛸 pexels.com](https://www.pexels.com/photo/photo-of-a-man-with-a-cap-posing-near-pipes-5752926/)")   
            
            with cols[1]: 
                r"""
                $$
                    \textsf{Rusty cast iron}: \quad e \approx 1.5 {\rm mm}
                $$
                """  
                st.image("https://images.pexels.com/photos/5589898/pexels-photo-5589898.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", use_column_width=True)
                st.caption(f"*Woman posing among pipes* [🛸 pexels.com](https://www.pexels.com/photo/woman-posing-among-pipes-5589898/)")   


    elif option == "Empirical relationships":

        r"""
        ## Hazen-Williams equation
        
        Used for:
        - Turbulent water flow
        - Circular pipes with diameter larger than 2 in
        - Water velocity less than 10 ft/s

        $$
            \textsf{BG}: \quad V = 1.318 \, C_{\texttt{HW}} \, R_h^{0.63} \, S^{0.54}
        $$
        
        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$C_{\texttt{HW}}$| Hazen-Williams coefficient | 🤔 |
        |$R_h$| Hydraulic radius | $ {\rm ft} $|
        |$S = \dfrac{h_f}{L}$| HGL slope | $ - $|

        &nbsp;

        """

        st.info("""
        - Show that $R_h = D/4$
        - Is the Hazen-Williams equation dimensionally homogeneous?
        - What would be the equivalent Hazen-Williams equation for SI units?
        """)

        r"""
        ****
        ## Manning equation
        
        Used for:
        - Turbulent water flow
        - Both free surface and pipe systems

        $$
            \textsf{SI}: \quad V = \dfrac{1}{n} \, R_h^{\tfrac{2}{3}} \, S^{\tfrac{1}{2}}
        $$

        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$n$| Manning's coefficient | 🤔 |
        |$R_h$| Hydraulic radius | $ {\rm m} $|
        |$S = \dfrac{h_f}{L}$| HGL slope | $ - $|

        &nbsp;
        """

        st.info("""
        - Is the Manning equation dimensionally homogeneous?
        - What would be the equivalent Manning equation for BG units?
        """)

    elif option == "Equations summary":

        r"""
        
        $$
            h_f = KQ^m
        $$
        
        |Equation|m|K (BG System)|K (SI System) |
        |:----|:---:|:---:|:---:|
        |Darcy-Weisbach | $2.0$ | $\dfrac{0.0252fL}{D^5}$ | $\dfrac{0.0826fL}{D^5}$ |
        |Hazen-Williams | $1.85$ | $\dfrac{4.73L}{D^{4.87}C^{1.85}_{\texttt{HW}}}$ | $\dfrac{10.7L}{D^{4.87}C^{1.85}_{\texttt{HW}}}$ |
        |Manning  | $2.0$ | $\dfrac{4.64n^2L}{D^{5.33}}$ | $\dfrac{10.3n^2L}{D^{5.33}}$ |
        """
        

        st.caption("*Source:* Table 3.4 - Class textbook")

        r"""
        *****
        ## Comparing head loss equations
        
        """

        cols = st.columns([0.5,2], gap="medium")

        with cols[0]:
            "****"
            f_dw = st.slider("Darcy-Weisbach -- $f$", 0.008, 0.1, 0.030, step=0.001, key="dw_f", format="%.3f")
            c_hw = st.slider(r"Hazen-Williams -- $C_{\texttt{HW}}$", 75, 160, 110, step=1, key="c_hw", format="%d")
            n_man = st.slider(r"Manning -- $n$", 0.009, 0.030, 0.010, step=0.001, key="n_man", format="%.3f")
            length = st.number_input("Pipe lenght -- $L$ [m]", 1, 100, 10, key="len_pipe", format="%d")
            diameter = st.number_input("Pipe diameter -- $D$ [mm]", 5.0, 250.0, 100.0, key="diam_pipe", format="%.0f")

        diameter /= 1000
        discharge = np.linspace(0.001, 0.005, 50)
        hf_dw = 0.0826 * f_dw * length / np.power(diameter, 5) * np.power(discharge, 2.0)
        hf_hw = 10.7 * length / (np.power(diameter, 4.87) * np.power(c_hw, 1.85))  * np.power(discharge, 1.85)
        hf_mn = 10.3 * np.power(n_man, 2) * length / np.power(diameter, 5.33)  * np.power(discharge, 2.0)

        discharge *= 1000.
        hovertemplate = "Q = %{x:.1f} L/s <br><b>h<sub>f</sub> = %{y:.2f} m</b>"
        fig = go.Figure([
            go.Scatter(
                x=discharge, 
                y=hf_dw,
                name="Darcy-Weisbach",
                hovertemplate=hovertemplate,
                line=dict(
                    width=5, 
                    color="#018749")
            ),
            go.Scatter(
                x=discharge, 
                y=hf_hw,
                name="Hazen-William",
                hovertemplate=hovertemplate,
                line=dict(
                    width=5, 
                    color="#FF8749")
            ),
            go.Scatter(
                x=discharge, 
                y=hf_mn,
                name="Manning",
                hovertemplate=hovertemplate,
                line=dict(
                    width=5, 
                    color="#8887FF")
            )
        ])

        fig.update_layout(
            title_text = '''Comparison between friction head loss equations''',
            height=650,
            yaxis=dict(
                title="Head loss <i>h<sub>f</sub></i> [m]",
                **axis_format),
            xaxis=dict(
                title="Discharge <i>Q</i> [m³/s]",
                **axis_format),
            legend=dict(
                title="Equation",
                font=dict(size=18),
                orientation="v",
                bordercolor="gainsboro",
                borderwidth=1,
                yanchor="top", y=0.99,
                xanchor="left", x=0.01
            ),
            hovermode='x',
            hoverlabel=dict(font_size=18),
        )

        with cols[1]: 
            st.plotly_chart(fig, use_container_width=True)

    elif option == "Accessories":

        r"""
        ## Pipe accessories
        """

        accesories_img_sources = [
            "https://images.pexels.com/photos/12142829/pexels-photo-12142829.jpeg",
            "https://images.pexels.com/photos/586019/pexels-photo-586019.jpeg",
            "https://images.pexels.com/photos/11142768/pexels-photo-11142768.jpeg",
            "https://images.pexels.com/photos/13312223/pexels-photo-13312223.jpeg"
        ]

        cols = cycle(st.columns(2))

        for col, img in zip(cols, accesories_img_sources):
            with col:
                st.image(img, use_column_width=True)
                st.caption(f"*Source* [🛸 https://www.pexels.com/]({img})")    

        r"""
        ****
        ## Head loss in accessories $\sum{h_a}$

        Also known as minor losses. 

        $$
            \begin{align*}
                h_1 + \dfrac{p_1}{\gamma} + \dfrac{V^2_1}{2g} = h_2 + \dfrac{p_2}{\gamma} + \dfrac{V^2_2}{2g} + \underbrace{h_f}_{\textsf{Friction}} + \underbrace{\sum{h_a}}_{\textsf{Accesories}}
            \end{align*}
        $$

        Just as the friction losses, minor losses are proportional to the velocity head.

        $$
            h_a = \underbrace{K_a}_{\substack{\textsf{Accesory} \\ \textsf{loss} \\ \textsf{coefficient}}} \, \dfrac{V^2}{2g}
        $$


        The energy conservation equation can be rewritten: 

        $$
            \begin{align*}
                h_1 + \dfrac{p_1}{\gamma} + \dfrac{V^2_1}{2g} = h_2 + \dfrac{p_2}{\gamma} + \dfrac{V^2_2}{2g} + \underbrace{f\dfrac{L}{D}\dfrac{V^2}{2g}}_{\textsf{Friction}} + \underbrace{\sum{K_a \dfrac{V^2}{2g}}}_{\textsf{Accesories}}
            \end{align*}
        $$

        *****

        """

        accesories_img_sources = [
            "https://images.thdstatic.com/productImages/4869fac1-e9fc-46ce-84a8-42dd89c9e11c/svn/black-the-plumber-s-choice-pvc-fittings-e83846x4-c3_600.jpg",
            "https://images.thdstatic.com/productImages/1471bb25-b360-437c-9faa-71d9a33a535b/svn/white-charlotte-pipe-pvc-fittings-pvc-00102-1850-fa_600.jpg",
            "https://images.thdstatic.com/productImages/732dd82d-0616-409b-885f-0cfcec42033b/svn/black-the-plumber-s-choice-pvc-fittings-e04848x4-1f_600.jpg",
            "https://images.thdstatic.com/productImages/7fba4b44-c32d-42ea-9f9f-3c6b52640184/svn/white-charlotte-pipe-pvc-fittings-pvc023001400hd-fa_600.jpg",
            "https://images.thdstatic.com/productImages/444a4229-e5b6-4f70-845f-5d2243284289/svn/black-southland-black-pipe-fittings-520-603hn-64_600.jpg",
            "https://images.thdstatic.com/productImages/522ab501-62f9-492e-8b40-d770f1382398/svn/white-charlotte-pipe-pvc-fittings-pvc006000800hd-64_600.jpg",
            "https://images.thdstatic.com/productImages/56a9d6e2-d72a-4913-8eae-11a9312e4d64/svn/apollo-ball-valves-94alf10301a-1f_600.jpg",
            "https://images.thdstatic.com/productImages/c0dcb0f9-eb3f-4809-b2ba-cb3663b8a29c/svn/everbilt-gate-valves-100-403eb-64_600.jpg",
            "https://images.thdstatic.com/productImages/86ad870a-a9df-43b2-87ec-56f3ee3c32b3/svn/sharkbite-check-valves-u2008-0000lfa-64_600.jpg",
            "https://images.thdstatic.com/productImages/7848050b-a7eb-45f4-9a9a-519f4de282b7/svn/water-source-pump-valves-pfv200-64_600.jpg"
        ]
        
        cols = cycle(st.columns(5))

        for col, img in zip(cols, accesories_img_sources):
            with col:
                st.caption(f"*Source:* [🏡]({img})")
                st.image(img, use_column_width=True)

        r"""
        ****
        ## Emmiters
        """

        cols = st.columns([1,2])
        
        with cols[0]:
            st.image("https://images.pexels.com/photos/10041326/pexels-photo-10041326.jpeg?auto=compress&cs=tinysrgb&w=420&h=250&dpr=2", use_column_width=True)
            st.caption("*Source* [🛸 pexels.com](https://images.pexels.com/photos/10041326/pexels-photo-10041326.jpeg)") 

        with cols[1]:
            r"""    
            > **Extracted from [EPANET User Manual](https://epanet22.readthedocs.io/en/latest/3_network_model.html)**
            >
            > *Emitters are devices associated with junctions that model the flow through a nozzle or orifice that discharges to the atmosphere.*
            > *The flow rate through the emitter varies as a function of the pressure available at the node:*
            > $$
            >     Q = Cp^{\alpha}
            > $$
            > |Parameter|Description|Units|
            > |:----:|:---|:---:|
            > |$Q$ | Discharge | ${\rm gpm}$ |
            > |$p$ | Pressure  | ${\rm psi}$ |
            > |$C$ | Emmiter coefficient | ${\rm gpm/psi}^{\alpha}$ |
            > |$\alpha = 0.5$  | Emmiter pressure exponent | - |
            > 
            > &nbsp;
            > 
            > *Emitters are used to model flow through sprinkler systems and irrigation networks. They can also be used to simulate leakage in a pipe 
            > connected to the junction (if a discharge coefficient and pressure exponent for the leaking crack or joint can be estimated) or compute a fire flow at the junction 
            > (the flow available at some minimum residual pressure).*

            """

    elif option == "Momentum and forces":
        r"""
        ## Momentum balance:

        $$
            \sum{\vec{F}} = \rho \, Q \, \left( \vec{V}_2 - \vec{V}_1\right)
        $$

        """

        cols = st.columns(2)

        with cols[0]:
            "### Thrust blocks"
            st.image("https://www.meyerfire.com/uploads/1/6/0/7/16072416/97-550-v2_orig.jpg", use_column_width=True)
            st.caption("*Source* [🛸 meyerfire.com](https://www.meyerfire.com/blog/a-new-thrust-block-calculator-part-i)") 

            st.image("https://www.ausflowsydney.com.au/wp-content/uploads/2018/07/6.-MaW-water-bends-1-e1546557720956.jpg", use_column_width=True)
            st.caption("*Source* [🛸 ausflowsydney.com.au](https://www.ausflowsydney.com.au/6-maw-water-bends/)") 

        with cols[1]:
            "### Pipe restraints"
            st.image("https://kannsupply.ca/wp-content/uploads/2020/02/1300C-Pipe-Restraint-4-42-1-scaled.jpeg", use_column_width=True)
            st.caption("*Source* [🛸 kannsypply.ca](https://kannsupply.ca/kann-products/1300c-pipe-restraint-4-42-2/)")

            st.image("https://images.assetsdelivery.com/compings_v2/designbydx/designbydx1505/designbydx150500087.jpg", use_column_width=True)
            st.caption("*Source* [🛸 stocklib.com](https://www.stocklib.com/media-40298637/failure-of-joint-restraint-ductile-water-pipe-600-mm-diameter.html)")


    else: 
        st.error("You should not be here!")

if __name__ == "__main__":
    main()