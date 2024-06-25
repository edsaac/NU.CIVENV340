import streamlit as st
from urllib.parse import urlparse
from scipy.stats import chi2
import numpy as np
import matplotlib.pyplot as plt
from dataretrieval import nwis
from datetime import timedelta
from typing import Literal


TOC = Literal[
    "Expected value",
    "Probability distributions",
    "Goodness of fit",
    "Return period",
    "Hydrological risk",
]


def page_week_10(option: TOC):
    st.title(option.replace("~", ""))

    if option == "Expected value":
        st.markdown(R"""
            **For a discrete process:**
            $$
                \mathrm{E}[X] = \sum_{i=1}^{\infty}{x_i p_i}
            $$

            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Expected value   | $\mathrm{E}[.]$   | Same of $x_i$  |
            |Random variable   | $X$   | -        |
            |Possible value   | $x_i$ | -        |
            |Probability      | $p_i$ | -        |

            """)

        img_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Largenumbers.svg"
        source = (
            "https://en.wikipedia.org/wiki/Expected_value#/media/File:Largenumbers.svg"
        )

        st.caption(
            rf"""
            **Rolls of a die:** convergence of sequence averages of rolls of a die to the expected value of 3.5 as the number of rolls (trials) grows.<br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_column_width=True)

        st.markdown(R"""
            **For a continous process:**
            $$
                \mathrm{E}[X] = \int_{-\infty}^{\infty}{x f(x) dx}
            $$
            
            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Expected value   | $\mathrm{E}[.]$   | Same of $x_i$  | 
            |Random variable   | $X$   | -        |
            |Possible value   | $x$ | -        |
            |Probability density function (pdf)| $f_X$ | -        |
            
            &nbsp;
            """)

        st.warning(
            """
            In hydrology, we are interested in determining how long it takes for a process to 
            exceed a certain value $x_T$, not in the value itself. 

            $$
                E[X > x_T]
            $$
            """
        )

    elif option == "Probability distributions":
        st.markdown(R"""
            ## Probability distribution functions (pdf)

            A pdf $f(x)$ describes the possible outcomes of a random process, if it satisfies 
            the Kolmogorov axioms

            - Probability is non-negative
            - No probability exceeds 1.0 
            - The cumulative probability is 1.0

            ### 🎲 Normal distribution
            
            $$
                f(x) = \dfrac{1}{\sigma\sqrt{2\pi}} \exp{\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)}
            $$

            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Outcome value   | $x$   | Same of process $X$ | 
            |Mean   | $\mu$   | Same of $x$ |
            |Standard deviation | $\sigma$ | Same of $x$ |
            |Variance | $\sigma^2$ | Same of $x^2$ |
            
            &nbsp;

            The probability that the value of an event lies between $x_1$ and $x_2$ is:

            $$
                P[x_1 \leq X \leq x_2] = \int_{x_1}^{x_2}f(x)dx
            $$
            """)

        st.warning(R"""       
            For a probability density function, the probability that the event takes a value equal to something is zero.
            $$
                P[X = x_1] = 0
            $$
            """)

        st.markdown(R"""
            ### 🎲 Log-normal distribution
            
            Sometimes, the logatithm of the hydrologic random variables are more likely to follow a normal distribution.

            $$
                f(x) = \dfrac{1}{x\sigma\sqrt{2\pi}} \exp{\left( -\dfrac{(\log{x} - \mu)^2}{2\sigma^2} \right)}
            $$

            ### 🎲 Gumbel distribution

            Also known as **Type-I generalized extreme value distribution**. 

            $$
                f(x) = y \left( \exp{\left( -y(x-u) - \exp{\left( -y(x-u) \right)} \right)} \right)
            $$

            With:

            - $y = {\pi}/({\sigma \sqrt{6}})$
            - $u = \mu - 0.45\sigma$
            &nbsp;

            ### 🎲 Log-Pearson Type III distribution

            $$
                f(x) = \dfrac{\nu^b (\log{x} - r)^{b-1} \exp{\left( -\nu(\log{x} - r) \right)}}{x\Gamma(b)}
            $$

            With:
            
            - $b = 4/G_l^2$
            - $\nu = \sigma/\sqrt{b}$
            - $r = \mu - \sigma\sqrt{b}$
            - $\Gamma$ is the [Gamma function](https://en.wikipedia.org/wiki/Gamma_function).

            """)

        st.info("""How many parameters does my pdf have?""")

        st.markdown(R"""
            ***********

            ## Cumulative distribution function (CDF)

            The probability that the random variable takes a value less or equal than a certain 
            value is given by:

            $$
                P[X \leq x_2] = \int_{-\infty}^{x_2}f(x)dx 
            $$
            
            The CDF is a function that represents that same probability: 

            $$
                F(x) = \int_{-\infty}^{x} f(u)du
            $$

            In hydrology, we are more interested in the complement to the CFD, i.e., the **exceedence probability**

            $$
                p(x) = 1.0 - F(x)
            $$
            """)

    elif option == "Goodness of fit":
        st.markdown(R"""
            How well does the data fit a given probability distribution? 

            1. Calculate the statistic $\chi^2$
            $$
                \chi^2 = \sum_{i=1}^{k} \dfrac{(O_i - E_i)^2}{E_i}
            $$

            2. Determine the degrees of freedom ($\mathsf{df}$)
            $$
                \mathsf{df} = k - \mathsf{params} - 1
            $$
            
            3. Chose a **significance level** ($\alpha$) for the test. $\alpha$ represents the probability that a rejected test actually corresponded to a 
            satisfactory distribution. This is refered to as a [type I error](https://en.wikipedia.org/wiki/Type_I_and_type_II_errors#Type_I_error), 
            or false positive. 

            4. Calculate the critical value for $\chi^2_\alpha$ from the $\chi^2$ probability 
            distribution

            5. The distribution is accepted if the **$\chi^2$ test** succeeds  
            $$
                \chi^2 < \chi^2_\alpha
            $$

            ****
            Calculating $\chi^2_{\alpha}$:
            """)

        cols = st.columns(2)

        with cols[0]:
            degree_freedom = st.number_input(r"$\mathsf{df}$", 1, 1000, 50, 1)

        with cols[1]:
            signif_alpha = st.number_input(r"$\alpha$", 0.0, 1.0, 0.10, 0.01)

        chi2_value = chi2.ppf(1.0 - signif_alpha, degree_freedom)

        st.latex(Rf"\chi^2_{{\alpha = {signif_alpha} }} = {chi2_value:.1f}")

        st.warning(R"""
            For a $\chi^2$ goodness of fit test, observations are assumed to be **independent**
            of each other. 
            """)

    elif option == "Return period":
        st.markdown(R"""
            ## Recurrence interval

            $$
                \tau: \textsf{ Time between ocurrences of } X>x_T
            $$

            There exists a probability distribution of $\tau$ that must have
            an associated expected value.

            $$
                \mathrm{E}[\tau] = \sum_{\tau=1}^{\infty}{\tau p_\tau} = E[X > x_T]
            $$
            """)

        img_url = "https://wires.onlinelibrary.wiley.com/cms/asset/4003beae-2074-4281-a8d9-60dce0cf0c1b/wat21340-fig-0001-m.jpg"
        source = "https://wires.onlinelibrary.wiley.com/doi/10.1002/wat2.1340"

        st.caption(
            rf"""
            **Time series of a stationary and independent process Z** (Volpi, 2019) <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_column_width=True)

        st.divider()
        st.markdown(R"""
            ## Return period

            $$
                T = \dfrac{1}{p}
            $$

            $$
                \mathrm{E}[X] = \dfrac{T}{\Delta \tau}
            $$
            
            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Expected value   | $\mathrm{E}[.]$   | Same of $x_i$  | 
            |Return period   | $T$   | Time |
            |Sampling rate   | $\Delta \tau$ | Time |

            &nbsp;
            
            """)

        img_url = "https://wires.onlinelibrary.wiley.com/cms/asset/c1a8e0cc-5f6c-4e53-9f7e-86cc0c0502cf/wat21340-toc-0001-m.jpg"
        source = "https://wires.onlinelibrary.wiley.com/doi/10.1002/wat2.1340"

        st.caption(
            rf"""
            **Return period and probability of failure** (Volpi, 2019) <br>
            Source: [{urlparse(source).hostname}]({source})
            """,
            unsafe_allow_html=True,
        )
        st.image(img_url, use_column_width=True)
        st.divider()

        st.markdown(R"""

            **Example**

            Consider the peak streamflow from USGS 03339000 VERMILION RIVER NEAR DANVILLE, IL.
            What is the return period of a streamflow of 20000 ft³/s?
            """)

        with st.echo():
            peaks, metadata = nwis.get_discharge_peaks("03339000")

        peaks["greater?"] = np.greater(peaks["peak_va"], 20_000)

        st.dataframe(
            peaks[["peak_va", "greater?"]], use_container_width=True, height=250
        )

        fig, ax = plt.subplots()
        ax.bar(peaks.index, peaks["peak_va"], width=timedelta(365))
        ax.set_xlabel("Year")
        ax.set_ylabel("Peak instantaneous discharge [ft³/s]")
        ax.set_title("USGS 03339000 VERMILION RIVER NEAR DANVILLE, IL")
        st.pyplot(fig)

    else:
        st.markdown(R"""
            ## Estimated Limiting Value (ELV)

            Defined as *"the largest magnitude possible for a hydrologic event at a given location,
            based on the best available hydrologic information"*.

            - **PMP**: [Probable maximum precipitation](https://www.nationalacademies.org/our-work/modernizing-probable-maximum-precipitation-estimation)
            - **PMF**: Probable maximum flood

            *****
            ## Hydrologic risk of failure $\bar{R}$

            $\bar{R}$ represents the probability that an event $X > x_T$
            occurs at least once in a period of $n$ years

            $$
                \bar{R} = 1 - \left(1 - P(X \geq x_T) \right)^n = 1 - \left(1 - \dfrac{1}{T} \right)^n
            $$

            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Hydrologic risk of failure   | $R$   | - | 
            |Expected life of the structure | $n$   | years | 
            |Return period | $T$   | years | 
            
            """)

        risk_value = st.number_input(r"$\bar{R}$", 0.0, 1.0, 0.60, 0.05, format="%.2f")

        design_life = np.geomspace(1, 1000, 50)
        return_period = np.geomspace(1, 1000, 50)
        nn, tt = np.meshgrid(design_life, return_period)
        risk = 1.0 - np.power(1.0 - 1.0 / tt, nn)
        fig, ax = plt.subplots()
        # levels = np.arange(0.05, 1.00, 0.10)
        levels = [risk_value]
        cs = ax.contour(nn, tt, risk, levels=levels, colors="k", label=r"$\bar{R}$")
        img = ax.pcolormesh(nn, tt, risk, vmin=0.00, vmax=1.00, alpha=0.5, cmap="jet")
        plt.colorbar(img, label=r"$\bar{R}$", shrink=0.5)
        ax.clabel(
            cs,
            levels=levels,
            inline=False,
            colors="w",
            fontsize=16,
            fmt="$\\bar{R}$ = %.2f",
        )
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(which="both", visible=True, lw=1, alpha=0.2, c="k")
        ax.set_xlabel(r"Design life $n$ [years]")
        ax.set_ylabel(r"Return period $T$ [years]")
        ax.set_title(r"Hydrological risk $\bar{R}$")
        st.pyplot(fig)

        st.info(
            R"""
            *Example:*

            A culvert has an expected life of 10 years. The acceptable risk of at least one event
            exceeding the culvert capacity during its desing life is 10%. What design period should be used?
            
            $$
                \bar{R} = 1 - \left( 1 - \dfrac{1}{T} \right)^n
            $$

            Find $T$ such that $\bar{R} = 0.10$

            """
        )

        st.markdown(R"""
            ## Safety factor and safety margin

            $$
                \mathsf{SF} = \dfrac{C}{L}
            $$
            
            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Safety factor   | $\mathsf{SF}$   | - | 
            |Actual capacity adopted in the project | $C$   | - | 
            |Hydrologic design value | $L$   | - | 

            $$
                \mathsf{SM} = C - L
            $$
            
            | Parameter | Symbol   | Units  |
            |:---------|:--------:|:------------------:|
            |Safety margin   | $\mathsf{SM}$   | - | 
            |Actual capacity adopted in the project | $C$   | - | 
            |Hydrologic design value | $L$   | - | 

            """)


if __name__ == "__page__":
    page_week_10()
