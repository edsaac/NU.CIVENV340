import streamlit as st
import pickle

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import numpy as np

from collections import namedtuple
Side = namedtuple("Side",["x","y"])
Point = namedtuple("Point", ["x","y"])

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
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ntrhqntu.json"  background="transparent"  speed="1.5"  style="width: 260px; height: 250px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=250, height=250)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [   
                "Smooth transitions",
                "Jumps and momentum conservation",
                "Uniform flow",
                "Gradually varied flow", 
                "Water profiles",
                "Free-surface calculation",
                "Sediments & rivers",
                "Lane's diagram",
                "Shear stress"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
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
    
    if option == "Smooth transitions":
        r"""
        ## 🌁 Contractions and expansions"""
        
        st.pyplot(draw_contraction())
        
        r"""
        Assuming that the energy losses through the contraction are negligible,

        $$
            E_1 = E_2
        $$

        Knowing $y_1$ and $Q$, $y_2$ can be predicted given a change in channel
        geometry (i.e., $b_2$ for a rectangular section).

        $$
            y_1 + \dfrac{Q^2}{2gA_1^2} = y_2 + \dfrac{Q^2}{2gA_2^2}
        $$

        The discharge is the same in the two sections, but the cross-sectional area
        will differ as the channel geometry differ. 

        """

        r"""
        ************
        ## 🪜 Steps
        """
        st.pyplot(draw_step())
        r"""
        Assuming that the energy losses through the step are negligible,

        $$
            E_1 = E_2 + \Delta z
        $$

        With $y_1$ and $Q$, $y_2$ can be predicted given a change in the
        bottom elevation (i.e., $\Delta z$).

        $$
            y_1 + \dfrac{Q^2}{2gA_1^2} = y_2 + \dfrac{Q^2}{2gA_2^2} + \Delta z
        $$

        The discharge is the same in the two sections, but the cross-sectional area
        will differ as the depth changes. 

        ************
        
        ### ⌛ Choking

        If the specific energy upstream is less than the required to pass through
        a given section, it will have to adjust itself by either:
        
        - Decreasing its discharge
        - Increasing its specific energy

        """


    elif option == "Jumps and momentum conservation":
        r"""
        ## Hydraulic jumps
        """
        cols = st.columns(2)

        with cols[0]:
            url = "https://www.youtube.com/watch?v=xTXQKeSZbGE"
            st.video(url)
            st.caption(f"Source: [youtube.com/@a-thaksalawa2483]({url})")

        with cols[1]:
            
            with st.expander("Experiment with dam:"):
                url = "https://www.youtube.com/watch?v=VU7UEiO6ijA"
                st.video(url)
                st.caption(f"Source: [youtube.com/@WakaWakaWakaW]({url})")

            with st.expander("Experiment in a flume:", expanded=True):
                url = "https://www.youtube.com/watch?v=uz7d_1KnbPM"
                st.video(url)
                st.caption(f"Source: [youtube.com/@WakaWakaWakaW]({url})")
                
        r"""
        Convert a high-velocity flow into a subcritical
        # """
        st.pyplot(draw_hydraulic_jump())

    elif option == "Uniform flow":
        r"""
        ## Uniform flow
        
        - The water depth $y$, the cross-sectional area $A$, the discharge $Q$ and the velocity profile $V(y,z)$
        remain constant over the channel lenght
        - The EGL, water surface and channel bottom are parallel
        $$
            S_0 = S_w = S_e
        $$
        
        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$S_0$| Channel bottom slope | - |
        |$S_w$| Water surface slope| - |
        |$S_e$| Energy line gradient | - |

        *****
        ### Chézy formula

        $$
            V = C_{\textsf{Chézy}} \, \sqrt{R_h \, S_e}
        $$
        
        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$V$| Mean velocity | Length/Time |
        |$C_{\textsf{Chézy}}$| Chézy's resistance factor | - |
        |$R_h$| Hydraulic radius | Length |
        |$S_e$| Energy line gradient | - |

        
        *****
        ### Manning equation

        $$
            V = \dfrac{k_\textsf{M}}{n} \, R_h^{\frac{2}{3}} \, \sqrt{S_e}
        $$
            
        |Parameter|Description|Units|
        |:---:|:---|:---:|
        |$V$| Mean velocity | Length/Time |
        |$k_\textsf{M} = \bigg\{ \substack{1.00 \, \mathrm{\sqrt[3]{m}/s} \\ \\ 1.49 \, \mathrm{\sqrt[3]{ft}/s}} $| Unit conversion factor.  | Length/Time |
        |$n$| Manning coefficient of roughness | - |
        |$R_h$| Hydraulic radius | Length |
        |$S_e$| Energy line gradient | - |
        
        &nbsp;

        In terms of discharge,

        $$
            Q = \dfrac{k_\textsf{M}}{n} \,A \, R_h^{\frac{2}{3}}\sqrt{S_e}
        $$
        """

        st.info(r"""
        - Who was Antoine de Chézy? 🇫🇷
        - How is Chézy formula derived?
        - Who was Robert Manning? 🇮🇪
        """,
        icon="🏞️")

        r"""
        *******
        ## Normal depth $y_n$
        
        Given a discharge $Q$ and a channel bottom slope $S_0$, the normal depth $y_n$
        satisfies the normal flow equation.

        ### For a rectangular section:
        """

        cols = st.columns([1.5, 2])

        with cols[0]: ## Channel options
            "#### Parameters"

            width = st.number_input("Width -- $b$ [m]", 0.1, 50.0, 3.0, 1.0, format="%.2f")
            discharge = st.number_input("Discharge -- $Q$ [m³/s]", 0.1, 200.0, 25.3, 1.0, format="%.1f")
            n_manning = st.number_input("Mannning coef. -- $n$ [-]", 0.010, 0.070, 0.022, 0.001, format="%.3f")
            slope = st.number_input("Bottom slope -- $S_0$ [-]", 0.0001, 0.1000, 0.0410, 0.0001, format="%.4f")
            initial_guess = st.number_input("Initial guess for $y_n$", 0.01, 50.0, 1.2, format="%.2f")
            method = st.selectbox("Root finding method:", ['hybr', 'lm'] )
    
        with cols[1]: ## Function def
            
            "#### Define equation to solve"
            with st.echo():
                def solve_normal_depth_rect_channel(
                    depth:float, 
                    width:float, 
                    discharge:float, 
                    n_manning:float, 
                    slope:float):
                    
                    k = 1.0 ## SI Units
                    area = width * depth
                    wetted_perim = width + 2*depth
                    hydr_radius = area/wetted_perim
                    calculated_discharge = k/n_manning * area * np.power(hydr_radius, 2/3) * np.sqrt(slope)
                    
                    return discharge - calculated_discharge
            
            "#### Call `scipy.root`"
            with st.echo():
                from scipy.optimize import root
                
                normal_depth = root(
                    solve_normal_depth_rect_channel,     
                    x0 = initial_guess,
                    args = (
                        width,
                        discharge,
                        n_manning,
                        slope
                    ),
                    method = method
                )

        
        with cols[0]: 
            "******"
            if normal_depth.success:
                st.metric("*Solved* $\; y_n$", f"{normal_depth.x[0]:.2f} m")
            else:
                st.error(r"""
                Something went wrong... 
                try changing the initial guess for $y_n$ or the root-finding method.
                """, icon="🧪")
        
        r"""
        *****
        ## Critical slope $S_c$
        
        It is the channel bottom slope that satisfies that
        
        $$
            y_c = y_n
        $$
        
        """

    elif option == "Gradually varied flow":
        r"""
        ## Gradually Varied Flow (GVF)
        
        Changes in water depth occur over long distances.  The total energy of the
        flow in a given section is

        $$
            H = z + y + \dfrac{Q^2}{2g\,A^2}
        $$

        Differentiating along the longitudinal distance $x$,

        $$
            \dfrac{dH}{dx} = \dfrac{dz}{dx} + \dfrac{dy}{dx} + \dfrac{-Q^2}{g\,A^3}\dfrac{dA}{dx}
        $$

        Rearanging for the water surface slope $dy/dx$,
        
        $$
            \dfrac{dy}{dx} = \dfrac{\dfrac{dH}{dx} - \dfrac{dz}{dx}}{1 - \dfrac{Q^2\,T}{g\,A^3}}
        $$ 

        | Parameter | Description   | Units  |
        |:---------:|:--------:|:------------------:|
        |$dy/dx = S_w$  | Slope of the water surface  | - | 
        |$dz/dx = S_0$  | Slope of the bottom channel | - | 
        |$dH/dx = S_e$  | Slope of the EGL | - | 
        |$Q$  | Discharge | Volume/Time | 
        |$A$  | Cross-sectional area | Area | 
        |$T$  | Top width | Length | 

        &nbsp;

        Or, 

        $$
            \dfrac{dy}{dx} = \dfrac{S_e - S_0}{1 - \dfrac{Q^2\,T}{g\,A^3}}
        $$

        &nbsp;

        Since the changes in depth occur in short distances, it can be assumed that
        $S_e$ could be calculated using a normal flow equation (i.e., Manning equation).
        
        ******
        ## Standard step method (finite difference)

        """
    elif option == "Water profiles":
        r"""
        ## Slope classification

        |Symbol| Name | In terms of bottom slope | In terms of depth |
        |:---:|:---|:----:|:---:|
        |$\mathtt{M}$| Mild | $S_0 < S_c$ | $y_n > y_c$ |
        |$\mathtt{C}$| Critical | $S_0 = S_c$ | $y_n = y_c$ |
        |$\mathtt{S}$| Steep | $S_0 > S_c$ | $y_n < y_c$ |
        |$\mathtt{H}$| Horizontal | $S_0 = 0$ | No normal flow |
        |$\mathtt{A}$| Adverse | $S_0 < 0$ | No normal flow |

        &nbsp;
        
        """
    elif option == "Free-surface calculation":
        r"### 🚧 Under construction 🚧"
    elif option == "Sediments & rivers":
        r"### 🚧 Under construction 🚧"
    elif option == "Lane's diagram":
        r"### 🚧 Under construction 🚧"
    elif option == "Shear stress":
        r"### 🚧 Under construction 🚧"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

@st.cache_data
def draw_contraction():

    side_down = Side(
        x= np.array([0,4,12,15]), 
        y = np.array([-3,-3,-2,-2])
    )

    side_up = Side(
        x = side_down.x, 
        y = -side_down.y
    )

    water_surface = Side(
        x = side_down.x,
        y = np.array([2,2,1,1])
    )

    fig, axs = plt.subplots(2,1, sharex=True, figsize=[8,10],
        gridspec_kw=dict(hspace=-0.2))

    ax = axs[0] ## Profile view
    ax.set_ylabel("Profile view", loc="center")

    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0], water_surface.y[0]+0.1, r"HGL", 
        ha="left", fontdict=dict(size=10, color="navy"))

    ## EGL
    ax.plot(water_surface.x, [3.5]*4, c="mediumseagreen", ls="dashed")
    ax.text(water_surface.x[0], 3.5 + 0.1, r"EGL", ha="left", fontdict=dict(size=10, color="mediumseagreen"))
    
    # Datum
    ax.axhline(-2, lw=1, color='k', ls="dashed", zorder=0)
    ax.text(1.0, -2 + 0.1, r"Datum", ha="center", fontdict=dict(size=8))

    # Sections annotations
    for i,x in enumerate(water_surface.x[1:3], start=1):
        
        ## Sections
        ax.plot([x]*2, [-4,4], ls="dotted", lw=1, c="gray")
        ax.text(x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray"))

        ## Depth
        ax.plot([x]*2, [-2, water_surface.y[i]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (water_surface.y[i]-2)/2, rf"$y_{i}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))

        ## Velocity head
        ax.plot([x]*2, [water_surface.y[i], 3.5], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (water_surface.y[i]+3.5)/2, rf"$\dfrac{{Q^2}}{{2gA^2_{i}}}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))


    # Channel bottom
    ax.axhline(y=-2, 
        lw=1.5, c="gray", 
        path_effects = [
            pe.withTickedStroke(offset=(0,0), angle=-45 ,spacing=6, length=3)
        ]
    )

    ax.text(water_surface.x[-1], -2 + 0.1, r"Channel bottom", ha="right", fontdict=dict(size=8, color="0.2"))
    
    # ax.fill_between(water_surface.x, -2, -2 - 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")

    # Final touches
    ax.set_ylim(-3, 5.0)

    #####################################
    ax = axs[1]  ## Plan view
    ax.set_ylabel("Plan view", loc="center")
    
    ## Channel borders
    ax.plot(side_down.x, side_down.y , 
        lw=1.5, c="gray",
        path_effects = [
            pe.withTickedStroke(offset=(0,0), angle=-45 ,spacing=6, length=3)
        ]
    )
    
    # ax.fill_between(side_down.x, side_down.y, side_down.y - 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")

    ax.plot(side_up.x, side_up.y , 
        lw=1.5, c="gray",
        path_effects = [
            pe.withTickedStroke(offset=(0,0), angle=45 ,spacing=6, length=3)
        ])
    
    # ax.fill_between(side_up.x, side_up.y, side_up.y + 0.4,
    #     hatch="////", ec="#00000030", fc="#ffffff")
    
    ## Section annotations
    for i,x in enumerate(side_down.x[1:3], start=1):
        
        ## Sections
        ax.plot([x]*2, [-4,4], ls="dotted", lw=1, c="gray")
        ax.text(x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray"))

        ## Width
        ax.plot([x]*2, [side_down.y[i], side_up.y[i]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, 0, rf"$b_{i}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))

    
    # Final touches
    #ax.legend(ncols=2, loc="upper right", bbox_to_anchor=(0.20, 0.95))
    ax.set_ylim(-5.0, 5.0)

    # Final touches for all axes
    for ax in axs:
        ax.set_xlim(side_down.x[0], side_down.x[-1])
        ax.set_aspect('equal')
        
        #ax.grid(True, color="lightgray")
        for spine in ax.spines: ax.spines[spine].set_visible(False)
        ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        ## Flow direction
        ax.text(side_down.x.mean(),0, r"$Q$", 
            ha="left", va="center", size=12,
            bbox=dict(
                boxstyle="rarrow,pad=0.3",
                fc="cornflowerblue",
                alpha=0.5,
                lw=0
            ))
    return fig

def draw_step():
    bottom = Side(
        x= np.array([0,4,12,15]), 
        y = np.array([-2,-2,-1,-1])
    )

    water_surface = Side(
        x = bottom.x,
        y = np.array([2,2,0.5,0.5])
    )


    fig, ax = plt.subplots()
    ax.set_ylabel("Profile view", loc="center")
    
    # Datum
    ax.axhline(-2, lw=1, color='k', ls="dashed", zorder=2)
    ax.text(bottom.x[-1], -2 + 0.1, r"Datum", ha="right", fontdict=dict(size=8))

    ## Bottom
    ax.plot(bottom.x, bottom.y, c="0.50", ls="dashed")
    ax.text(bottom.x[0], bottom.y[0] + 0.1, r"Channel bottom", ha="left", fontdict=dict(size=8, color="0.2"))
    ax.fill_between(bottom.x, bottom.y, bottom.y - 0.4,
        hatch="////", ec="#00000030", fc="#ffffff")

    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0], water_surface.y[0]+0.1, r"HGL", 
        ha="left", fontdict=dict(size=10, color="navy"))

    ## EGL
    ax.plot(water_surface.x, [4]*4, c="mediumseagreen", ls="dashed")
    ax.text(water_surface.x[0], 4 + 0.1, r"EGL", ha="left", fontdict=dict(size=10, color="mediumseagreen"))
    

    # Sections annotations
    
    ## Depth
    ax.plot([bottom.x[-2]]*2, [-2, bottom.y[-2]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
    ax.text(bottom.x[-2]+0.2, bottom.y.mean(), rf"$\Delta z$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))
    
    for i,x in enumerate(bottom.x[1:3], start=1):
        
        ## Sections
        ax.plot([x]*2, [-4,4], ls="dotted", lw=1, c="gray")
        ax.text(x, 4.2, f"Section\n{i}", ha="center", fontdict=dict(size=10, color="gray"))

        ## Depth
        ax.plot([x]*2, [bottom.y[i], water_surface.y[i]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (bottom.y[i]+water_surface.y[i])/2, rf"$y_{i}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))

        ## Velocity head
        ax.plot([x]*2, [water_surface.y[i], 4], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (water_surface.y[i] + 4)/2, rf"$\dfrac{{Q^2}}{{2gA^2_{i}}}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))


    # Final touches for all axes
    ax.set_xlim(bottom.x[0], bottom.x[-1])
    ax.set_ylim(-2.5,5)
    ax.set_aspect('equal')
    #ax.grid(True, color="lightgray")
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    ## Flow direction
    ax.text(bottom.x.mean(),0, r"$Q$", 
        ha="left", va="center", size=12,
        bbox=dict(
            boxstyle="rarrow,pad=0.3",
            fc="cornflowerblue",
            alpha=0.5,
            lw=0
        ))
    return fig

@st.cache_data
def get_realistic_water():
    import requests
    from PIL import Image
    from io import BytesIO
    
    url = "https://cdn4.iconfinder.com/data/icons/water-waves-design/1470/tornado_blue_water_wave_spiral_hurricane_logo-512.png"
    r = requests.get(url, stream=True)

    img = Image.open(BytesIO(r.content), formats=["png", "jpg"])

    return img

def realistic_water(ax:plt.Axes, p:Point, size:float):
    
    if "realistic_water" not in st.session_state:
        img = get_realistic_water()
        st.session_state.realistic_water = img
    else:
        img = st.session_state.realistic_water
        
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox

    imagebox = OffsetImage(img, zoom=size, cmap="bone_r")

    ax.add_artist(
        AnnotationBbox(
            imagebox, 
            p,
            frameon=False,
            zorder=1
        )
    )

@st.cache_data
def draw_hydraulic_jump():
    bottom = Side(
        x= np.array([0,4,6,8,10,15]), 
        y = np.array([-2,-2,-2,-2,-2,-2])
    )

    water_surface = Side(
        x = bottom.x,
        y = np.array([-1, -1, -1, 2, 2, 2])
    )

    energy_line = Side(
        x = bottom.x,
        y = np.array([5,5,5,4,4,4])
    )

    fig, ax = plt.subplots()
    ax.set_ylabel("Profile view", loc="center")
    
    # Datum
    ax.axhline(-2, lw=1, color='k', ls="dashed", zorder=2)
    ax.text(bottom.x[-1], -2 + 0.1, r"Datum", ha="right", fontdict=dict(size=8))

    ## Bottom
    ax.plot(
        bottom.x, bottom.y, 
        c="0.50", lw=1.5, 
        path_effects = [
            pe.withTickedStroke(offset=(0,0), angle=-45 ,spacing=6, length=1.5)
        ]
    )
    
    ax.text(
        bottom.x[0], bottom.y[0] + 0.1, 
        r"Channel bottom", 
        ha="left", 
        fontdict=dict(
            size=8, 
            color="0.2"
        )
    )
    
    ## Water surface
    ax.plot(water_surface.x, water_surface.y, lw=3, c="navy")
    ax.text(
        water_surface.x[0], water_surface.y[0]+0.1, r"HGL", 
        ha="left", fontdict=dict(size=10, color="navy"))

    n_eddies = 10
    for x,y,s in zip(np.linspace(6,8,n_eddies), np.linspace(-1,2,n_eddies), np.random.random(n_eddies)):
        realistic_water(ax, Point(x+.1,y-.2), 0.05*s)

    # EGL
    ax.plot(energy_line.x, energy_line.y, c="mediumseagreen", ls="dashed")
    ax.text(energy_line.x[0], energy_line.y[0] + 0.1, r"EGL", ha="left", fontdict=dict(size=10, color="mediumseagreen"))
    ax.axhline(energy_line.y[0], c="mediumseagreen", ls="dashed", lw=0.5, alpha=0.5)
    

    # Sections annotations
    
    ## Energy loss
    ax.plot([energy_line.x[-2]]*2, [energy_line.y[-1], energy_line.y[0]], marker="o", ms=4 ,lw=1, c='darkslategray', ls=":")
    ax.text(energy_line.x[-2] + 0.2, energy_line.y[2:4].mean(), rf"$h_L$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))
    
    for i,x in enumerate([4,10], start=2):
        
        ## Sections
        ax.plot([x]*2, [-4,5.5], ls="dotted", lw=1, c="gray")
        ax.text(x, 5.6, f"Section\n{i-1}", ha="center", fontdict=dict(size=10, color="gray"))

        ## Depth
        ax.plot([x]*2, [bottom.y[i], water_surface.y[i]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (bottom.y[i]+water_surface.y[i])/2, rf"$y_{i-1}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=12))

        ## Velocity head
        ax.plot([x]*2, [water_surface.y[i], energy_line.y[i]], marker="o", ms=4 ,lw=2, c='darkslategray', ls=":")
        ax.text(x+0.2, (water_surface.y[i] + energy_line.y[i])/2, rf"$\dfrac{{Q^2}}{{2gA^2_{i-1}}}$", ha="left", va="center", fontdict=dict(color='darkslategray', size=10))

    # Flow direction
    ax.text(bottom.x.max()-2, 0, r"$Q$", 
        ha="right", va="center", size=12,
        bbox=dict(
            boxstyle="rarrow,pad=0.3",
            fc="cornflowerblue",
            alpha=0.5,
            lw=0
        )
    )

    # Final touches for all axes
    ax.set_xlim(bottom.x[0], bottom.x[-1])
    ax.set_ylim(-2.5,5.6)
    ax.set_aspect('equal')
    #ax.grid(True, color="lightgray")
    for spine in ax.spines: ax.spines[spine].set_visible(False)
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    return fig

if __name__ == "__main__":
    main()