import streamlit as st
from streamlit.navigation.page import StreamlitPage

from functools import partial
from typing import Callable, get_args
from PIL import Image, ImageOps

from book.pages import (
    page_week_01,
    page_week_02,
    page_week_03,
    page_week_04,
    page_week_05,
    page_week_06,
    page_week_07,
    page_week_08,
    page_week_09,
    page_week_10,
)
from book.common import page_config_common, apply_css_style, sidebar_common, badges


def generate_list_of_pages(page_week: Callable) -> list[StreamlitPage]:
    list_of_topics = get_args(page_week.__annotations__["option"])

    pages = []

    for i, topic in enumerate(list_of_topics, start=1):
        if not topic.startswith("~"):
            pages.append(
                st.Page(
                    partial(page_week, topic),
                    title=(title := f"{topic}"),
                    url_path=title.replace(" ", "_").replace("-", "").strip().lower(),
                    icon=":material/article:",
                )
            )

        else:
            pages.append(
                st.Page(
                    partial(page_week, topic),
                    title=(title := " - " + topic.replace("~", "")),
                    url_path=title.replace("-", "").strip().replace(" ", "_").lower(),
                    icon="🐍",
                )
            )

    return pages


def entrypoint_page():
    
    with st.popover("About", use_container_width=False):
        
        st.image('./book/assets/img/in_class_l.jpg', caption="During a lecture")

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

        left_col, right_col = st.columns(2)
        left_col.markdown(badges["this_repo"])
        right_col.markdown(badges["other_stuff"])
    
    st.title("🌊 Hydraulics with Python 🌊")
    st.header("", anchor=False, divider="blue")

    st.markdown(
        R"""
        This material was first made to support the course 
        :violet[CIV-ENV 340: Hydraulics and Hydrology] that I taught during 
        the Spring quarter of 2023 at Northwestern University. It is divided
        in the ten weeks of the quarter, covering concepts in hydraulics of
        presurized pipe systems, open channel flow, and basic hydrology. This
        class included short computational projects, in which we...

        > - built our own EPANET® using scipy
        > - made a gradually-variable flow profiles calculator
        > - delineated a real watershed programatically
        > - queried and analyzed stream gauge data from USGS

        The pages marked with a 🐍 indicate the projects involving using Python.
        The rest correspond to supplemental material for the lectures, like 
        diagrams and interactive plots.

        """
    )


def main():
    st.set_page_config(**page_config_common)
    apply_css_style()
    sidebar_common()

    entry_page = st.Page(
        entrypoint_page, title="Introduction", default=True, icon=":material/book_2:"
    )

    nav = st.navigation(
        {
            "Cover": [entry_page],
            "Week 1 - Basics & introduction": generate_list_of_pages(page_week_01),
            "Week 2 - Head losses": generate_list_of_pages(page_week_02),
            "Week 3 - Pipe networks": generate_list_of_pages(page_week_03),
            "Week 4 - Pumps": generate_list_of_pages(page_week_04),
            "Week 5 - Open-channel flow": generate_list_of_pages(page_week_05),
            "Week 6 - More channel flow": generate_list_of_pages(page_week_06),
            "Week 7 - Hydraulic structures": generate_list_of_pages(page_week_07),
            "Week 8 - Watersheds and water cycle": generate_list_of_pages(page_week_08),
            "Week 9 - Hydrology and engineering": generate_list_of_pages(page_week_09),
            "Week 10 - Basics of probability": generate_list_of_pages(page_week_10),
        }
    )

    nav.run()


if __name__ == "__main__":
    main()
