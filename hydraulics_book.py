import streamlit as st
import os
from book.pages import all_pages
from book.common import page_config_common, apply_css_style, sidebar_common, badges


def entrypoint_page():

    st.title("🌊 Hydraulics and Hydrology with Python 🌊", anchor="Hydraulics and Hydrology with Python")
    st.markdown("&nbsp;")
    
    left_col, right_col = st.columns([2, 1])

    with right_col:
        with st.container(border=True):
            st.image("./book/assets/img/in_class_l.jpg", caption="During a lecture")

            st.html(
                R"""
                <p style="text-align:center">
                    By Edwin Saavedra Cifuentes, PhD.
                </p>
                <p style="text-align:center; font-size:0.8rem; line-height:0.9rem;>
                <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
                    <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" />
                </a>
                <br />This work is licensed under a 
                <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
                    Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
                </a>.
                </p>
                """
            )

            left_subcol, right_subcol = st.columns(2)
            left_subcol.markdown(badges["this_repo"])
            right_subcol.markdown(badges["other_stuff"])

    with left_col:
        st.markdown(
            R"""
            This material was first made to support the course 
            :violet[CIV-ENV 340: Hydraulics and Hydrology] that I taught during 
            the Spring quarter of 2023 at Northwestern University. It is divided
            in the ten weeks of the quarter, covering concepts in hydraulics of
            presurized pipe systems, open channel flow, and basic hydrology. This
            class included short computational projects, in which we...
            """
        )

        st.page_link(
            all_pages["Week 3 - Pipe networks"]["~Building an EPANET"],
            label=":violet-background[... built our own EPANET® using scipy]",
            use_container_width=True,
        )

        st.page_link(
            all_pages["Week 6 - More channel flow"]["~Solve IVP"],
            label=":violet-background[... made a gradually-variable flow profiles calculator]",
            use_container_width=True,
        )

        st.page_link(
            all_pages["Week 8 - Watersheds and water cycle"]["~Watershed delimitation"],
            label=":violet-background[... delineated a real watershed programatically]",
            use_container_width=True,
        )

        st.page_link(
            all_pages["Week 9 - Hydrology and engineering"]["~Rating curve"],
            label=":violet-background[... queried and analyzed stream gauge data from USGS]",
            use_container_width=True,
        )

        st.markdown("""
            The pages marked with a 🐍 indicate the projects involving using Python.
            The rest correspond to supplemental material for the lectures, like 
            diagrams and interactive plots.
            """)


def main():
    st.set_page_config(**page_config_common)
    apply_css_style()
    sidebar_common()

    entry_page = st.Page(
        entrypoint_page, title="Introduction", default=True, icon=":material/book_2:"
    )

    all_pages.update({"Cover": {"Introduction": entry_page}})

    pages_for_nav = {k: list(v.values()) for k, v in all_pages.items()}
    nav = st.navigation(pages_for_nav)
    nav.run()


if __name__ == "__main__":
    
    if not st.session_state.get("set_mplrc", False):
        os.environ["MATPLOTLIBRC"] = (
            os.getcwd() + "/book/assets/matplotlib/matplotlibrc"
        )
        st.session_state.set_mplrc = True

    main()
