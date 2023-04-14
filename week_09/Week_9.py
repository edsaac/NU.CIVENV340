import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
from urllib.parse import urlparse

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
        <lottie-player src="https://assets9.lottiefiles.com/packages/lf20_wvlrz62s.json"  background="transparent"  speed="3.0"  style="width: 200px; height: 200px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=200)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "Infiltration",
                "Green & Ampt model",
                "SCS Curve Number",
                "Design runoff",
                "Time of concentration",
                "Rational method"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
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
    
    if option == "Infiltration":
        r"""
        ## Infiltration
        
        """
    
    elif option == "Green & Ampt model":
        r"""
        ## Green & Ampt model
        """
        
        img_url = "https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/files/19695384/138249905/1/1680200741692/image-2023-3-30_11-25-41.png"
        source = "https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/infiltration-and-runoff-volume/green-and-ampt-loss-model"
        st.caption(rf"""
            **Green and Ampt Infiltration Model** <br>
            Source: [{urlparse(source).hostname}]({source})
            """, unsafe_allow_html=True
        )
        st.image(img_url, use_column_width=True)

        r"""
        #### Infiltration capacity
        $$
            f_p = \dfrac{K(z+\psi)}{z}
        $$

        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$f_p$| Infiltration capacity | Length/Time |
        |$\psi$| Characteristic suction head | Length |
        |$K$| Hydraulic conductivity | Length/Time |
        |$z$| Depth of the wetted zone | Length |

        &nbsp;
        #### Actual infiltration

        $$
            f = \begin{cases}
            i & i < f_p
            \\
            f_p & i > f_p
            \end{cases}
        $$

        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$f_p$| Infiltration capacity | Length/Time |
        |$f$| Actual rate of infiltration | Length/Time |
        |$i$| Rainfall intensity | Length/Time |

        &nbsp;
        #### Excess rainfall

        $$
            i_e = i - f
        $$

        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$i_e$| Rate of excess rain | Length/Time |
        |$i$| Rainfall intensity | Length/Time |
        |$f$| Actual rate of infiltration | Length/Time |


        &nbsp;
        #### Infiltration over time

        $$
            \Delta z = \dfrac{f \Delta t}{n\left( 1 - S_i \right)}
        $$
        
        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$\Delta z$| Increase of the wet front depth  | Length |
        |$\Delta t$| A time interval | Time |
        |$S_i$| Initial water saturation | Water vol. / Voids vol. |
        |$n$| Porosity | Voids vol. / Bulk vol. |

        &nbsp;

        $$
            F = \sum{f \Delta t}
        $$
        
        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$F$| Cumulative depth of water infiltrated from $t=0$  | Length |
        
        &nbsp;
        #### Wet front depth

        $$
             z = \dfrac{F}{n\left( 1 - S_i \right)}
        $$

        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$F$| Cumulative depth of water infiltrated from $t=0$  | Length 

        """




    elif option == "SCS Curve Number":
        r"""
        ## Soil Conservation Service Method
        
        $$
            R 
            = 
            \begin{cases}
            \begin{array}{ccl}
            0 & \quad & P \leq I_a
            \\
            \dfrac{\left( P - I_a \right)^2}{P - I_a + S}
            & \quad & P > I_a
            \end{array}
            \end{cases}
        $$

        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$R$| Rainfall excess → Runoff | Inches |
        |$P$| Cumulative rainfall | Inches |
        |$I_a = 0.2S$| Initial abstraction | Length |
        |$S = \dfrac{1000}{\texttt{CN}} - 10$| Soil-moisture storage deficit | - |
        |$\texttt{CN}$| Curve Number | - |

        &nbsp;
        """

        st.pyplot(plot_curve_number())

        r"""
        ****
        ### $\texttt{CN}$: Curve Number

        """

        with open("assets/tables/SCS_curve_number.html") as f:
            cn_table = f.read()
        
        st.markdown(cn_table, unsafe_allow_html=True)

    elif option == "Design runoff":
        r"""
        ## Hydrograph
        
        $$
            \textsf{Total runoff} = \textsf{Base flow} + \textsf{Direct runoff}
        $$
        """
        st.pyplot(plot_hydrograph(), use_container_width=True)

    elif option == "Time of concentration":
        r"""
        ## Time of concentration $T$

        > *Time it takes runoff to reach the design point from the most hydrologically remote point in the watershed*

        $$
        \begin{array}{rl}
            T =& \left(\substack{\textsf{Overland} \\ \textsf{flow}}\right)_t 
              + \left(\substack{\textsf{Shallow} \\ \textsf{flow}}\right)_t 
              + \left(\substack{\textsf{Open-channel} \\ \textsf{flow}}\right)_t  \\
            \\
            T =& T_{t_1} + T_{t_2} + T_{t_3}
        \end{array}
        $$

        ****
        ### Overland flow
        $$
            T_{t_1} = \dfrac{0.007\left( nL \right)^{0.8}}{P_2^{0.5} S^{0.4}}
        $$
        
        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$T_{t_1}$| Overland flow travel time | hr |
        |$L$| Flow length | ft |
        |$P_2$| 2-year, 24-hr rainfall | in |
        |$n$| Manning's coefficient | - |
        |$S$| Land slope | - |

        ****
        ### Shallow concentrated flow
        $$
            V = 16.1345 \sqrt{S}
        $$
        
        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$V$| Average velocity | ft/s |
        |$S$| Land slope | - |

        ****
        ### Open-Channel flow
        
        $$
            V = \dfrac{1.49}{n}R_h^{2/3}\sqrt{S_e}
        $$
        |Parameter|Description|Units|
        |:--------:|:----|:----:|
        |$V$| Average velocity | ft/s |
        |$R_h$| Hydraulic radius | ft |
        |$S_e$| Energy grade line slope | - |
        |$n$| Manning's coefficient | - |

        """
    elif option == "Rational method":
        r"""
        ## Rational method

        $$
            Q_{\textsf{Peak}} = C \, I \, A
        $$
        
        |Parameter|Description|Units|Notes|
        |:--------:|:----|:----:|:----|
        |$Q_\textsf{Peak}$| Peak discharge | acre-in/hr |  |
        |$C$| Runoff coefficient | - | Measure of land *imperviousness* |
        |$I$| Average rainfall intensity | in/hr | Obtained from an IDF curve |
        |$A$| Basin area | acres | It should be small (less htan 200 acres) |
        
        
        """

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

def plot_hydrograph():
    from scipy.stats import beta
    
    α, β = 2.0, 5.0
    mean, var = beta.stats(α, β, moments='mv')
    x = np.linspace(beta.ppf(0.01, α, β), beta.ppf(0.999, α, β), 100)
    y = beta.pdf(x, α, β) + 0.5


    fig,axs = plt.subplots(2,1, figsize=(8,8), gridspec_kw=dict(height_ratios=[1,10], hspace=0), sharex=False)

    # Hidrograph    
    ax = axs[1]
    time = np.concatenate([
        xsmol := np.linspace(0,0.2,10),
        x + 0.2
    ])

    discharge = np.concatenate([
        (xsmol-0.31)**2 + 0.5,
        y
    ])

    baseflow = (time-0.31)**2 + 0.5
    baseflow = np.where(baseflow<discharge, baseflow, discharge)
    imax = np.argmax(discharge)

    ax.plot(time, baseflow, c='k', ls="dotted")
    ax.plot(time, discharge, lw=3, c='k')

    ax.fill_between(time, discharge, baseflow, hatch="/", fc="violet", alpha=0.2)
    
    ax.text(0.43, 1.5, "Volume of \n direct \n surface \n runoff", 
        fontsize=14,
        ha='center', va='center', 
        bbox=dict(
            boxstyle="round4", 
            fc="w", ec="k"
        )
    )


    ## Annotations
    ax.text(0.18, 1.5, "Rising limb", rotation=75)
    ax.text(0.65, 1.5, "Recession", rotation=-55)

    ax.text(
        0.65, 0.60, 
        "Base flow", 
        rotation=10,
        bbox=dict(
            boxstyle="round4", 
            fc="w", ec="k", ls="dotted",
        )
    )


    ax.annotate(
        "Peak", 
        (time[imax], discharge.max()), 
        (0.6, 3.0), 
        fontsize=16,
        # bbox=dict(boxstyle="round4", fc="w"),
        arrowprops=dict(
            arrowstyle="-|>",
            connectionstyle="arc3,rad=0.2", 
            fc="w"
        )
    )
    

    ax.set_xlabel("Time [hr]", fontsize=14)
    ax.set_ylabel("Discharge [m³/s]", fontsize=14)
    
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 3.5)
    
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])

    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.spines.left.set_edgecolor("gray")
    ax.set_facecolor("#ffff1100")

    # Precipitation
    ax = axs[0]
    time_rain = [0.01, 0.06, 0.11, 0.16, 0.21]
    rain = [1.5, 2.7, 4.0, 2.1, 0.7]

    ax.bar(time_rain, rain, 0.048, align='edge', clip_on=False)

    ax.spines.bottom.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.spines.left.set_edgecolor("purple")

    ax.set_ylabel("Rainfall [in]")
    
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])
    ax.xaxis.set_ticks([])
    
    ax.set_ylim(2.0, 0)
    ax.set_xlim(0, 1.0)

    return fig

@st.cache_data
def plot_curve_number():
    curve_numbers = np.arange(100, 19, -10)
    rainfall = np.linspace(0,12,128)
    from matplotlib.ticker import MaxNLocator
    fig,ax = plt.subplots(figsize=[8,6])

    ax.set_prop_cycle(
        plt.cycler(
            "color", 
            plt.cm.cividis(
                np.linspace(0,1,len(curve_numbers))
            )
        )
    )    

    for cn in curve_numbers:
        storage_deficit = 1000./cn - 10
        initial_abstraction = 0.2 * storage_deficit
        runoff = np.where(
            rainfall >= initial_abstraction,
            np.power(rainfall - initial_abstraction, 2) / (rainfall - initial_abstraction + storage_deficit),
            0
        )
        ax.plot(rainfall, runoff, label=f"{cn}", lw=2)

    ax.legend(title="Curve Number", loc="center left", bbox_to_anchor=(1.0, 0.5))
    
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.set_ylim(0,8)
    ax.set_xlim(0,12)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.5)
    ax.set_ylabel("Runoff \t $R$ [in]", fontsize=14)
    ax.set_xlabel("Rainfall \t $P$ [in]", fontsize=14)

    return fig

if __name__ == "__main__":
    main()