import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import numpy as np
from dataretrieval import nwis
from urllib.parse import urlparse
from datetime import date

import pandas as pd
from scipy.optimize import curve_fit


def rating_curve():
    
    img_url = "./book/assets/img/RatingCurve_02215500.png"
    source = "https://waterwatch.usgs.gov/"

    st.caption(
        rf"""
        **Rating curve for the Ocmulgee River, GA** <br>
        Source: [{urlparse(source).hostname}]({source})
        """,
        unsafe_allow_html=True,
    )
    st.image(img_url, use_column_width=True)

    st.divider()
    st.header("About the site")

    cols = st.columns([1, 2], vertical_alignment="center")
    
    # Specify the USGS site number/code
    site_id = cols[0].selectbox("Site number ID", ["02215500"])

    cols[1].info(
        """
        See query documentation at [osi.usgs.gov](https://owi.usgs.gov/R/training-curriculum/usgs-packages/dataRetrieval-readNWIS/index.html#readnwisrating)
        """
    )

    img_url = "https://c1.staticflickr.com/7/6064/6037331688_17b4c881df_b.jpg"
    source = "https://flickr.com/photos/alan_cressler/6037331688"

    st.caption(
        rf"""
        **Ocmulgee River Train Swing Bridge, Ocmulgee River, Lumber City, Telfair and Jeff Davis Counties, GA**<br>
        Source: [{urlparse(source).hostname}]({source})
        """,
        unsafe_allow_html=True,
    )
    st.image(img_url, use_column_width=True)

    st.markdown(
        """
        <iframe src="https://www.google.com/maps/embed?pb=!4v1684686947687!6m8!1m7!1spJqaWeiIkdWa9jYr_jRi6g!2m2!1d31.9199824386102!2d-82.67446321198821!3f236.12162750392207!4f-5.393784221498308!5f0.7820865974627469" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("&nbsp;")
    st.link_button(
        "Check it out at `waterdata.usgs.gov`",
        "https://waterdata.usgs.gov/monitoring-location/02215500/#parameterCode=00065&period=P7D",
        use_container_width=True,
    )

    st.divider()
    st.header("Using USGS `dataretrieval`")

    with st.echo():
        query = nwis.get_ratings(site=site_id, file_type="exsa")

    data = query[0]
    metadata = query[1]
    with st.expander("Query metadata"):
        st.code(metadata.comment, language=None, line_numbers=True)

    st.dataframe(query[0], use_container_width=True)

    with st.expander("Query definitions"):
        """
        - `INDEP` is the gage height in feet
        - `DEP` is the streamflow in cubic feet per second
        - `STOR` “*” indicates a fixed point of the rating curve, NA for non-fixed points
        - `SHIFT` indicates shifting in rating for the corresponding INDEP value
        - `CORR` are the corrected values of INDEP
        - `CORRINDEP` are the corrected values of CORR
        """

    y = data["INDEP"]
    Q = data["DEP"]

    fig, ax = plt.subplots()
    ax.plot(Q, y, c="gray", lw=3, label="USGS Rating curve")
    ax.set_xlabel("Discharge (ft³/s)")
    ax.set_ylim(-5, 30)
    ax.set_ylabel("Gage height (ft)")
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(True, which="both", axis="both")
    ax.set_title("OCMULGEE RIVER AT LUMBER CITY, GA")
    ax.legend()

    tabs = st.tabs(["linear", "semilog"])
    with tabs[0]:
        ax.set_xlim(600, 110_000)
        st.pyplot(fig)

    with tabs[1]:
        ax.set_xlim(600, 200_000)
        ax.set_xscale("log")
        st.pyplot(fig)

    st.divider()
    st.header("Getting the field measurements")

    start, end = st.date_input(
        "Date range",
        [date(2010, 1, 1), date(2023, 5, 1)],
        date(1950, 1, 1),
        date(2023, 5, 21),
    )
    with st.echo():
        field_query = nwis.get_discharge_measurements(
            sites=site_id, start=start.isoformat(), end=end.isoformat()
        )

    field_data = field_query[0]
    field_metadata = field_query[1]

    with st.expander("Query metadata"):
        st.code(field_metadata.comment, language=None, line_numbers=True)
        # st.code(field_metadata.header, language=None, line_numbers=True)
        st.code(field_metadata.url, language=None, line_numbers=True)

    st.dataframe(field_data, use_container_width=True)

    ## Remove the None data rows
    field_data = field_data.dropna()
    y_field = field_data["gage_height_va"]
    Q_field = field_data["discharge_va"]

    fig, ax = plt.subplots()
    ax.grid(True, which="both", axis="both", zorder=1)
    ax.plot(Q, y, c="gray", lw=3, label="USGS Rating curve", zorder=2)
    ax.scatter(
        Q_field, y_field, label="Field measurements", c="k", marker="x", zorder=5
    )
    ax.set_xlabel("Discharge (ft³/s)")
    ax.set_ylim(-5, 30)
    ax.set_ylabel("Gage height (ft)")
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.set_title("OCMULGEE RIVER AT LUMBER CITY, GA")
    ax.legend()

    tabs = st.tabs(["linear", "semilog"])
    with tabs[0]:
        ax.set_xlim(600, 110_000)
        st.pyplot(fig)

    with tabs[1]:
        ax.set_xlim(600, 200_000)
        ax.set_xscale("log")
        st.pyplot(fig)

    st.divider()
    st.header("Fitting an equation")
    st.latex("\log{Q} \propto H \implies Q = a \exp(b\,H) + c")

    with st.echo():

        def my_power_law(x, a, b, c):
            return a * np.exp(b * x) + c

    popt, pcov = curve_fit(my_power_law, xdata=y_field, ydata=Q_field, p0=[1, 1, -1])

    a, b, c = popt

    cols = st.columns(3)
    with cols[0]:
        st.metric("$a$", f"{a:.2E}")
    with cols[1]:
        st.metric("$b$", f"{b:.2E}")
    with cols[2]:
        st.metric("$c$", f"{c:.2E}")

    y_calc = np.linspace(-5, 30, 100)
    Q_calc = my_power_law(y_calc, *popt)

    fig, ax = plt.subplots()
    ax.grid(True, which="both", axis="both", zorder=1)

    ax.plot(Q, y, c="gray", lw=2, label="USGS Rating curve", zorder=2)
    ax.plot(Q_calc, y_calc, lw=2, c="cornflowerblue", label="Fitted curve", zorder=4)
    ax.scatter(
        Q_field, y_field, label="Field measurements", c="k", marker="x", zorder=5
    )

    ax.set_xlabel("Discharge (ft³/s)")
    ax.set_ylim(-5, 30)
    ax.set_ylabel("Gage height (ft)")
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(True, which="both", axis="both")
    ax.set_title("OCMULGEE RIVER AT LUMBER CITY, GA")
    ax.legend()

    tabs = st.tabs(["linear", "semilog"])
    with tabs[0]:
        ax.set_xlim(600, 110_000)
        st.pyplot(fig)

    with tabs[1]:
        ax.set_xlim(600, 200_000)
        ax.set_xscale("log")
        st.pyplot(fig)

    st.subheader("Error estimation")

    st.markdown(
        R"""
        How sensitive is the prediction to changes in each of the parameters?
        
        **Covariance matrix:**
        """
    )

    pd_cov = pd.DataFrame(pcov, index=[*"abc"], columns=[*"abc"])
    st.table(
        pd_cov.style.format("{:.3E}").background_gradient(
            axis=None, vmin=0, vmax=1e4, cmap="YlGnBu"
        )
    )

    st.markdown("**Error on the parameters:**")

    perr = np.sqrt(np.diag(pcov))
    pd_perr = pd.DataFrame(perr, index=[*"abc"])
    st.table(pd_perr.style.format("{:.3E}"))

    st.subheader("Coefficient of determination")
    st.markdown("How far are the predictions from the observations?")
    st.latex(R"R^2 = 1 - \dfrac{\sum_i{(y_i - f_i)^2}}{\sum_i{(y_i - \bar{y})^2}}")

    st.markdown(
        R"""
        - If the predicted values exactly match the observations, $R^2 = 1$
        - If the prediction is always the mean of the observations, $R^2 = 0$
        - Worse predictions will have $R^2 < 0$

        **In hydrological models**, this metric is called the Nash-Sutcliffe model efficiency
        coefficient (NSE).

        """
    )

    Q_field_calc = my_power_law(y_field, *popt)

    residual_sum_squares = np.power(Q_field - Q_field_calc, 2)
    variance = np.power(Q_field - np.average(Q_field), 2)
    R2 = 1.0 - np.sum(residual_sum_squares) / np.sum(variance)

    st.metric("$R^2$", f"{R2:.3}")



if __name__ == "__main__":
    rating_curve()
