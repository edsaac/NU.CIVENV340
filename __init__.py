import streamlit as st

def sidebar_common():
    with st.sidebar:

        cols = st.columns(2)
        with cols[0]:
            st.markdown(
                """
                [![Github Repo](https://img.shields.io/static/v1?label=&message=Repository&color=black&logo=github)](https://github.com/edsaac/NU.CIVENV340)
                """
            )

        with cols[1]:
            st.markdown(
                """
                [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)
                """
            )