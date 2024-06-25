import streamlit as st
from streamlit.components.v1 import iframe


def find_critical_depth():

    st.markdown(
        R"""
        ## Solving an implicit equation
        
        $$
            \textsf{Critical depth - Trapezoidal section:} \quad \dfrac{Q^2}{g} = A^2 D_h
        $$

        With, """
    )

    cols = st.columns(2)
    with cols[0]:  ## Area equation
        st.markdown(
            r"""
            $$
                A = (b+my)y
            $$
            """
        )

    with cols[1]:  ## Hydraulic depth eq.
        st.markdown(
            r"""
            $$
                D_h = \dfrac{(b+my)y}{b + 2my}
            $$
            """
        )

    st.markdown(
        R"""
        ## 1️⃣ Rearange equation to equal zero

        $$
            \dfrac{Q^2}{g} - A^2 D_h = 0
        $$

        ****
        ## 2️⃣ Define a function with the equation
        """
    )

    with st.echo():
        g = 9.81  # - m/s²

        def critical_depth_trapezoid(yc, b, m, Q):
            area = (b + m * yc) * yc
            hyd_depth = area / (b + 2 * m * yc)
            return (Q**2) / g - (area**2 * hyd_depth)

    st.markdown(
        r"""
        ****
        ## 3️⃣ Call `scipy.optimize.root`
        """
    )

    iframe(
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy-optimize-root",
        height=500,
        width=500,
        scrolling=True,
    )
    "*****"

    cols = st.columns(2)
    with cols[0]:
        bottom_width = st.slider(
            "Bottom width -- $b$", 0.5, 50.0, 5.0, 0.1, format="%.1f"
        )
        side_slope = st.slider("Side slope -- $m$", 0.0, 10.0, 2.0, 0.1, format="%.1f")
        flow_rate = st.slider("Flow rate -- $Q$", 1.0, 500.0, 20.0, 0.1, format="%.1f")
        method = st.selectbox("Root finding method:", ["hybr", "lm"])
        initial_guess = st.number_input(
            r"Initial guess -- $y_{c, \textsf{ guess}}$", 0.0, 100.0, 1.0
        )

    with cols[1]:
        "&nbsp;"
        "&nbsp;"

        with st.echo():
            from scipy.optimize import root

            y_c = root(
                critical_depth_trapezoid,
                x0=initial_guess,
                args=(bottom_width, side_slope, flow_rate),
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
        st.metric(r"$y_{c, \textsf{ guess}}$", f"{initial_guess:.2f} m")

    with cols[1]:
        if y_c.success:
            st.metric("$y_c$", f"{y_c.x[0]:.2f} m")
        else:
            st.error(
                r"""
            Something went wrong... 
            try changing the initial guess for $f$ or the root-finding method.
            """,
                icon="🧪",
            )


if __name__ == "__main__":
    find_critical_depth()
