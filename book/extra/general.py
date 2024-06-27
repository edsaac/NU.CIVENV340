import streamlit as st
from typing import Literal

TOC = Literal[
    "System of Units",
]


def appendices(option: TOC):
    st.title(option.replace("~", ""))

    if option == "System of Units":
        tabs = st.tabs(["**Normal conditions**", "**Standard conditions**"])

        with tabs[0]:
            st.markdown(R"""

                | Parameter           | Symbol | Units       | SI                                | BG                                     |
                |:--------------------|:------:|:-----------:|:---------------------------------:|:--------------------------------------:|
                |Temperature          | $T$    | Temperature | $20.2 \, \degree\textrm{C}$       | $68.4 \, \degree\textrm{F}$            |
                |Atmospheric pressure | $p_{\rm atm}$    | Force/Area  | $1.014 \times 10^{5} \, \textrm{Pa}$ | $14.7 \, \textrm{lb}/\textrm{in}^2$ |
                |Atmospheric pressure | $p_{\rm atm}/\gamma$ | Lenght  | $10.3 \, \textrm{m H}_2\textrm{O}$   | $33.8 \, \textrm{ft H}_2\textrm{O}$ |
                |Gravitational acceleration| $g$ | Lenght/Time²  | $9.81 \, \textrm{m}/\textrm{s}^2$| $32.2 \, \textrm{ft}/\textrm{s}^2$ |

                ****

                | Water property    | Symbol   | Units              | SI                                                 | BG                                                   |
                |:---------         |:--------:|:------------------:|:--------------------------------------------------:|:----------------------------------------------------:|
                |Specific weight    | $\gamma$ | Force/Lenght       | $9790                \, \textrm{N}/\textrm{m}^3$   | $62.3                \, \textrm{lb}/\textrm{ft}^3$   |
                |Density            | $\rho$   | Mass/Volume        | $998                 \, \textrm{kg}/\textrm{m}^3$  | $1.94                \, \textrm{slug}/\textrm{ft}^3$ |
                |Viscosity          | $\mu$    | Force · Time/Area  | $1.00 \times 10^{-3} \, \textrm{N s}/\textrm{m}^2$ | $2.09 \times 10^{-5} \, \textrm{lb s}/\textrm{ft}^2$ |
                |Kinematic viscosity| $\nu$    | Area/Time          | $1.00 \times 10^{-6} \, \textrm{m}^2/\textrm{s}$   | $1.08 \times 10^{-5} \, \textrm{ft}^2/\textrm{s}$    |
                |Surface tension    | $\sigma$ | Force/Lenght       | $7.13 \times 10^{-2} \, \textrm{N}/\textrm{m}$     | $4.89 \times 10^{-3} \, \textrm{lb}/\textrm{ft}^{-3}$|
                |Vapor pressure     |   -      | Force/Area         | $2.37 \times 10^{3}  \, \textrm{N}/\textrm{m}^2$   | $3.44 \times 10^{-1} \, \textrm{lb}/\textrm{in}^2$   |
                """)

        with tabs[1]:
            st.markdown(R"""

                | Parameter           | Symbol | Units       | SI                                | BG                                     |
                |:--------------------|:------:|:-----------:|:---------------------------------:|:--------------------------------------:|
                |Temperature          | $T$    | Temperature | $4 \, \degree\textrm{C}$       | $39.2 \, \degree\textrm{F}$            |
                |Atmospheric pressure | $p_{\rm atm}$    | Force/Area  | $1.014 \times 10^{5} \, \textrm{Pa}$ | $14.7 \, \textrm{lb}/\textrm{in}^2$ |
                |Atmospheric pressure | $p_{\rm atm}/\gamma$ | Lenght  | ❓   | ❓ |
                |Gravitational acceleration| $g$ | Lenght/Time²  | $9.81 \, \textrm{m}/\textrm{s}^2$| $32.2 \, \textrm{ft}/\textrm{s}^2$ |

                ****

                | Water property    | Symbol   | Units              | SI                                                 | BG                                                   |
                |:---------         |:--------:|:------------------:|:--------------------------------------------------:|:----------------------------------------------------:|
                |Specific weight    | $\gamma$ | Force/Lenght       | $9810                \, \textrm{N}/\textrm{m}^3$   | $62.4                \, \textrm{lb}/\textrm{ft}^3$   |
                |Density            | $\rho$   | Mass/Volume        | $1000                 \, \textrm{kg}/\textrm{m}^3$ | $1.94                \, \textrm{slug}/\textrm{ft}^3$ |
                |Viscosity          | $\mu$    | Force · Time/Area  | $1.57 \times 10^{-3} \, \textrm{N s}/\textrm{m}^2$ | $3.28 \times 10^{-5} \, \textrm{lb s}/\textrm{ft}^2$ |
                |Kinematic viscosity| $\nu$    | Area/Time          | $1.57 \times 10^{-6} \, \textrm{m}^2/\textrm{s}$   | $1.69 \times 10^{-5} \, \textrm{ft}^2/\textrm{s}$    |
                |Surface tension    | $\sigma$ | Force/Lenght       | $7.36 \times 10^{-2} \, \textrm{N}/\textrm{m}$     | $5.04 \times 10^{-3} \, \textrm{lb}/\textrm{ft}^{-3}$|
                |Vapor pressure     |   -      | Force/Area         | $8.21 \times 10^{2}  \, \textrm{N}/\textrm{m}^2$   | $1.19 \times 10^{-1} \, \textrm{lb}/\textrm{in}^2$   |
                """)
