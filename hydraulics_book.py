import streamlit as st
from streamlit.navigation.page import StreamlitPage

from functools import partial
from typing import Callable, get_args

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
from book.common import page_config_common, apply_css_style, sidebar_common


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
    st.title("Hydraulics with Python")

    "Made by [Edwin Saavedra Cifuentes](https:edsaac.github.io)"


def main():
    st.set_page_config(**page_config_common)
    apply_css_style()
    sidebar_common()

    entry_page = st.Page(
        entrypoint_page, title="Cover", default=True, icon=":material/book_2:"
    )

    nav = st.navigation(
        {
            "Main": [entry_page],
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
