import streamlit as st
import pickle
from urllib.parse import urlparse


def main():
    with open("assets/page_config.pkl", "rb") as f:
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
        <lottie-player src="https://assets4.lottiefiles.com/private_files/lf30_nep75hmm.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=100)

        "### Select a topic:"
        option = st.radio(
            "Select a topic:",
            ["Expected value", "Return period", "Hydrological risk"],
            label_visibility="collapsed",
        )

        "***"
        st.image(
            "https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg"
        )

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
            r"""[![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""

    ####################################################################

    if option == "Expected value":
        r"""
        ## Expected value

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

        """

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

        """
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
        """

        st.warning(
            """
        
        In hydrology, we are interested in determining how long it takes for a process to 
        exceed a certain value $x_T$, not in the value itself. 

        $$
            E[X > x_T]
        $$
        """
        )

    elif option == "Return period":
        r"""
        ## Recurrence interval

        $$
            \tau: \textsf{ Time between ocurrences of } X>x_T
        $$

        There exists a probability distribution of \tau that must have
        an associated expected value.

        $$
            \mathrm{E}[\tau] = \sum_{\tau=1}^{\infty}{\tau p_\tau} = E[X > x_T]
        $$
        """

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

        "****"
        r"""
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
        
        """

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

    else:
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"


if __name__ == "__main__":
    main()
