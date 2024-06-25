import streamlit as st
from streamlit.components.v1 import iframe
import numpy as np


def using_scipy_root():
    st.markdown(
        R"""
        ## Solving an implicit equation
        
        $$
            \textsf{Colebrook-White eq:} \quad \dfrac{1}{\sqrt{f}} = -2\log\left( \dfrac{e}{3.7\,D} + \dfrac{2.51}{R_e \, \sqrt{f}} \right)
        $$

        ## 1️⃣ Rearange equation to equal zero

        $$
            -2\log\left( \dfrac{e}{3.7\,D} + \dfrac{2.51}{R_e \, \sqrt{f}} \right) - \dfrac{1}{\sqrt{f}} = 0
        $$

        ****
        ## 2️⃣ Define a function with the equation
        """
    )

    with st.echo():

        def colebrook_white_equation(fguess, rel_rough, reynolds):
            if fguess <= 0 :
                return np.nan
            
            return (
                -2 * np.log10(rel_rough / 3.7 + 2.51 / (reynolds * np.sqrt(fguess)))
            ) - (1.0 / np.sqrt(fguess))

    st.markdown(
        R"""
        ****
        ## 3️⃣ Call `scipy.optimize.root`
        """
    )

    url = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy-optimize-root"
    iframe(url, height=500, width=500, scrolling=True)
    st.divider()

    cols = st.columns(2)

    with cols[0]:
        relative_roughness = st.number_input(
            "Relative roughness -- $e/D$", 1e-6, 0.05, 1e-5, format="%.2e", key="cw_eD"
        )

        Reynolds = st.number_input(
            "Reynolds number -- $R_e$", 1e3, 1e9, 1e6, format="%.2e", key="cw_Re"
        )

        initial_guess = st.number_input(
            "Initial guess for $f$", 0.004, 0.10, 0.05, format="%.4f"
        )

        method = st.selectbox("Root finding method:", ["hybr", "lm"])

    with cols[1]:
        st.markdown("&nbsp;")

        with st.echo():
            from scipy.optimize import root

            friction_factor = root(
                colebrook_white_equation,
                x0=initial_guess,
                args=(
                    relative_roughness,
                    Reynolds,
                ),
                method=method,
            )

    st.markdown(
        R"""
        ****
        ## 🏁 Print final results
        """
    )

    cols = st.columns(2)

    with cols[0]:
        st.metric("*Initial guess* f", f"{initial_guess:.5f}")

    with cols[1]:
        if friction_factor.success:
            st.metric("*Solution*", f"{friction_factor.x[0]:.5f}")
        else:
            st.error(
                r"""
                Something went wrong... 
                try changing the initial guess for $f$ or the root-finding method.
                """,
                icon="🧪",
            )

    st.markdown(
        R"""
        ****
        ## 👾 What about `scipy.optimize.fsolve`
        """
    )

    url = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html#scipy.optimize.fsolve"
    iframe(url, height=500, width=500, scrolling=True)

    with st.expander("About the algorithm"):
        url = "https://www.math.utah.edu/software/minpack/minpack/hybrd.html"
        iframe(url, height=500, width=550, scrolling=True)


if __name__ == "__main__":
    using_scipy_root()
