import streamlit as st
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import matplotlib as mpl
from urllib.parse import urlparse
from typing import Literal

from .subpages import rating_curve


TOC = Literal[
    "Infiltration",
    "Green & Ampt model",
    "SCS Curve Number",
    "Design runoff",
    "Time of concentration",
    "Rational method",
    "~Rating curve",
]


def page_week_09(option: TOC):
    st.title(option.replace("~", ""))
    print(mpl.matplotlib_fname())
    if option == "Infiltration":
        img_url = (
            "https://onlinemanuals.txdot.gov/TxDOTOnlineManuals/TxDOTManuals/hyd/images/4-9.png"
        )
        source = "https://onlinemanuals.txdot.gov/TxDOTOnlineManuals/TxDOTManuals/hyd/hydrograph_method.htm"
        st.caption(
            rf"""
            **Water mass balance** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.markdown(
            R"""
            ### Horton's equation

            $$
                f(t) = f_c + (f_0 - f_c)\exp{(-kt)}
            $$
            
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$f(t)$| Infiltration rate | Length/Time |
            |$f_0$| Initial infiltration rate | Length/Time |
            |$f_c$| End infiltration rate | Length/Time |
            |$k$| Decay rate | 1/Time |
            
            &nbsp;
            
            **Infiltration capacity** refers to the maximum rate of infiltration. It decreases
            as the soil moisture content increases. Runoff occurs with precipitation rate 
            exceeds the infiltration rate. 

            ### Accumulated infiltration

            $$
                F(t) = \int_0^t f(\tau) d\tau
            $$
            
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$F(t)$| Total accumulation in a period of time | Length |

            &nbsp;
            
            Horton's equation is a solution of the differential equation:

            $$
                \dfrac{\partial \theta}{\partial t} = D \dfrac{\partial^2 \theta}{\partial z^2}
            $$
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$\theta$| Soil water content | Volume/Volume |
            |$z$| Depth | Length |
            |$t$| Time | Time |
            
            &nbsp;

            ****
            ### Infiltrometer
            """
        )

        img_url = "https://upload.wikimedia.org/wikipedia/commons/a/aa/Single_ring.JPG"
        source = "https://en.wikipedia.org/wiki/Infiltrometer"
        st.caption(
            rf"""
            **Single ring infiltrometer** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.divider()
        st.warning("Infiltration rate and hydraulic conductivity are similar, but distinct! ")

    elif option == "Green & Ampt model":
        img_url = "https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/files/19695384/138249905/1/1680200741692/image-2023-3-30_11-25-41.png"
        source = "https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/infiltration-and-runoff-volume/green-and-ampt-loss-model"
        st.caption(
            rf"""
            **Green and Ampt Infiltration Model** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.markdown(
            R"""
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
        )

    elif option == "SCS Curve Number":
        st.markdown(
            R"""
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
        )

        st.pyplot(plot_curve_number())

        st.divider()
        st.subheader(R"$\texttt{CN}$: Curve Number")

        with open("./book/assets/tables/SCS_curve_number.html") as f:
            cn_table = f.read()

        st.markdown(cn_table, unsafe_allow_html=True)

        st.divider()
        source = "https://directives.sc.egov.usda.gov/22162.wba"
        st.caption(
            rf"""
            Source: Urban Hydrology for Small Watersheds <br>
            USDA - Natural Resources Conservation Service <br>
            [Technical Release TR-55 (June 1986)]({source})
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            R"""
            ### Factors to consider in determining CN

            - Hydrologic soil groups (HSG)
                - A, B, C or D
                - According to the minimum infiltration rate obtained from bare soil after prolonged wetting
            - Cover type
                - Vegetation, bare soil or impervious
            - Treatment
                - Management of cultivated areas
            - Hydrologic condition
                - Effects of cover type on infiltration and runoff
                - Estimated from density of vegetation and residue cover
            - Antecedent runoff condition (ARC)
                - Attempts to account for CN variation from storm to storm
            - Impervious areas conectedness 
            """
        )

        st.divider()
        img_url = "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41597-019-0155-x/MediaObjects/41597_2019_155_Fig2_HTML.png"
        source = "https://www.nature.com/articles/s41597-019-0155-x"
        st.caption(
            rf"""
            Source: GCN250, new global gridded curve numbers for hydrologic modeling and design <br>
            Global curve number maps for dry, average and wet ARC <br>
            [*Jaafar et al. (2019)*]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        img_url = "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41597-019-0155-x/MediaObjects/41597_2019_155_Fig3_HTML.png"
        source = "https://www.nature.com/articles/s41597-019-0155-x"
        st.caption(
            rf"""
            Source: GCN250, new global gridded curve numbers for hydrologic modeling and design <br>
            CN map for selected river basins around the world <br>
            [*Jaafar et al. (2019)*]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

    elif option == "Design runoff":
        st.markdown(
            R"""
            ## Hydrograph

            $$
                \textsf{Total runoff} = \textsf{Base flow} + \textsf{Direct runoff}
            $$
            """
        )
        st.pyplot(plot_hydrograph(), use_container_width=True)

        cols = st.columns([1, 2])

        with cols[0]:
            st.info(
                """
                Check this example from 
                [usgs.gov](https://www.usgs.gov/special-topics/water-science-school/science/base-flow-rivers)
                """
            )

        with cols[1]:
            st.info(
                """
                Some definitions:
                - **TRH**: Total runoff hydrograph
                - **DRH**: Direct runoff hydrograph
                    - The volume of direct surface runoff is equal to the excess rainfall
                    times the area of the catchment.
                    - That is, assuming rainfall has a uniform spatial distribution. 
                - **BF**: Base flow
                """
            )

        st.markdown(
            R"""
            **********
            ## Unit hydrograph

            It is the conceptual direct runoff hydrograph (DRH) resulting form a rainfall *excess* of
            unit depth and a given duration.
            
            $$
                \textsf{UH}_{\Delta D}: \textsf{Unit Hydrogram}_{\textsf{Duration of rainfall excess}}
            $$

            A $\textsf{UH}$ can be constructed from rainfall and discharge measurements, if there
            is available data for rainfall events of the duration of interest and the intensity was
            constant over that period of time. 
            """
        )

        _, col, _ = st.columns(3)
        with col:
            st.warning(
                r"""
                Assuming:
                - Linearity
                - Superposition
                """
            )

        st.markdown(
            R"""
            ### Synthetic unit hydrograph (SCS Method)

            - **Time to peak:** Elapsed time between the start of the effective rainfall and
            the peak discharge

            $$
                T_p = \dfrac{\Delta D}{2} + T_L
            $$

            $$
                \Delta D = 0.133 T_c
            $$

            $$
                T_L = 0.6 T_c
            $$
            
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$T_p$| Time to peak | hr |
            |$\Delta D$| Duration of the **effective rainfall** | hr |
            |$T_L$| Lag time | hr |
            |$T_c$| Time of concentration | hr |

            &nbsp;

            $$
                q_p = \dfrac{K_p A}{T_p}
            $$

            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$q_p$| Peak discharge | cfs/in |
            |$A$| Drainage area | mi² |
            |$K_p = 484$| An empirical constant | hehe |

            """
        )

    elif option == "Time of concentration":
        st.markdown(
            R"""
            ## Time of concentration $T_c$

            > *Time it takes runoff to reach the design point from the most hydrologically remote point in the watershed*

            $$
            \begin{array}{rl}
                T_c =& \left(\substack{\textsf{Overland} \\ \textsf{flow}}\right)_t 
                + \left(\substack{\textsf{Shallow} \\ \textsf{flow}}\right)_t 
                + \left(\substack{\textsf{Open-channel} \\ \textsf{flow}}\right)_t  \\
                \\
                T_c =& T_{c_1} + T_{c_2} + T_{c_3}
            \end{array}
            $$

            ****
            ### Overland flow
            $$
                T_{c_1} = \dfrac{0.007\left( nL \right)^{0.8}}{P_2^{0.5} S^{0.4}}
            $$
            
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$T_{c_1}$| Overland flow travel time | hr |
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

            ******

            ### SCS empirical equation

            $$
                T_c = \dfrac{2.586L^{0.8} \left[ \dfrac{S}{25.4} + 1 \right]^{0.7}}{1140 \sqrt{Y}}
            $$
            |Parameter|Description|Units|
            |:--------:|:----|:----:|
            |$T_c$| Time of concentration| hr |
            |$L$| Length of the longest flow path in the watershed| ft |
            |$S$| Soil-moisture deficit at the time runoff begins $\dag$| in |
            |$Y$| Average watershed slope| percentage |
            |$\mathrm{CN}$| Curve Number| - |

            $$
                ^\dag \quad S = \dfrac{1000 - 10\mathrm{CN}}{\mathrm{CN}}
            $$
            
            """
        )

    elif option == "Rational method":
        cols = st.columns([2, 1])

        with cols[0]:
            st.markdown(
                R"""
                $$
                    Q_{\textsf{Peak}} = C \, I \, A
                $$

                |Parameter|Description|Units|Notes|
                |:--------:|:----|:----:|:----|
                |$Q_\textsf{Peak}$| Peak discharge | acre-in/hr |  |
                |$C$| Runoff coefficient | - | Measure of land *imperviousness* |
                |$I$| Average rainfall intensity | in/hr | Obtained from an IDF curve |
                |$A$| Basin area | acres | It should be small (less than 200 acres) |

                &nbsp;

                """
            )

        with cols[1]:
            img_url = "http://onlinemanuals.txdot.gov/txdotmanuals/hyd/images/4-8.png"
            source = "http://onlinemanuals.txdot.gov/txdotmanuals/hyd/rational_method.htm"
            st.caption(
                rf"""
                **Rational method steps** <br>
                Source: [{urlparse(source).hostname}]({source})
                """,
                unsafe_allow_html=True,
            )
            st.image(img_url, use_container_width=True)

        st.markdown(
            R"""
            ******
            #### Rainfall intensity
            It is the average precipitation rate for a given duration
            and frequency. The duration is usually related to the time of concentration.
            
            #### Runoff coefficients
            Depends on the land use and type of soil.
            """
        )

        img_url = "book/assets/img/Runoff_coeffs.png"
        source = "https://virginiadot.org/business/resources/LocDes/DrainageManual/chapter6.pdf"
        st.caption(
            rf"""
            **Runoff coefficients** <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_container_width=True)

        st.warning(
            r"""
                $200 \textsf{ acres} \approx 80 \textsf{ ha} \approx 151 \textsf{ football fields}$     
             """
        )

    elif option == "~Rating curve":
        rating_curve()

    else:
        st.error("You should not be here!")


def plot_hydrograph():
    α, β = 2.0, 5.0
    mean, var = beta.stats(α, β, moments="mv")
    x = np.linspace(beta.ppf(0.01, α, β), beta.ppf(0.999, α, β), 100)
    y = beta.pdf(x, α, β) + 0.5

    fig, axs = plt.subplots(
        2,
        1,
        figsize=(8, 8),
        gridspec_kw=dict(height_ratios=[1, 10], hspace=0),
        sharex=False,
    )

    # Hidrograph
    ax = axs[1]
    time = np.concatenate([xsmol := np.linspace(0, 0.2, 10), x + 0.2])

    discharge = np.concatenate([(xsmol - 0.31) ** 2 + 0.5, y])

    baseflow = (time - 0.31) ** 2 + 0.5
    baseflow = np.where(baseflow < discharge, baseflow, discharge)
    imax = np.argmax(discharge)

    ax.plot(time, baseflow, c="k", ls="dotted")
    ax.plot(time, discharge, lw=3, c="k")

    ax.fill_between(time, discharge, baseflow, hatch="/", fc="violet", alpha=0.2)

    ax.text(
        0.43,
        1.5,
        "Volume of \n direct \n surface \n runoff",
        fontsize=14,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round4", fc="w", ec="k"),
    )

    ## Annotations
    ax.text(0.18, 1.5, "Rising limb", rotation=75)
    ax.text(0.65, 1.5, "Recession", rotation=-55)

    ax.text(
        0.65,
        0.60,
        "Base flow",
        rotation=10,
        bbox=dict(
            boxstyle="round4",
            fc="w",
            ec="k",
            ls="dotted",
        ),
    )

    ax.annotate(
        "Peak",
        (time[imax], discharge.max()),
        (0.6, 3.0),
        fontsize=16,
        # bbox=dict(boxstyle="round4", fc="w"),
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.2", fc="w"),
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

    # Precipitation
    ax = axs[0]
    time_rain = [0.01, 0.06, 0.11, 0.16, 0.21]
    rain = [1.5, 2.7, 4.0, 2.1, 0.7]

    ax.bar(time_rain, rain, 0.048, align="edge", clip_on=False)

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


@st.cache_resource
def plot_curve_number():
    curve_numbers = np.arange(100, 19, -10)
    rainfall = np.linspace(0, 12, 128)
    from matplotlib.ticker import MaxNLocator

    fig, ax = plt.subplots(figsize=[8, 6])

    ax.set_prop_cycle(plt.cycler("color", plt.cm.cividis(np.linspace(0, 1, len(curve_numbers)))))

    for cn in curve_numbers:
        storage_deficit = 1000.0 / cn - 10
        initial_abstraction = 0.2 * storage_deficit
        runoff = np.where(
            rainfall >= initial_abstraction,
            np.power(rainfall - initial_abstraction, 2)
            / (rainfall - initial_abstraction + storage_deficit),
            0,
        )
        ax.plot(rainfall, runoff, label=f"{cn}", lw=2)

    ax.legend(title="Curve Number", loc="center left", bbox_to_anchor=(1.0, 0.5))

    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.set_ylim(0, 8)
    ax.set_xlim(0, 12)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.5)
    ax.set_ylabel("Runoff \t $R$ [in]", fontsize=14)
    ax.set_xlabel("Rainfall \t $P$ [in]", fontsize=14)

    return fig
