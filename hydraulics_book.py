import streamlit as st
from streamlit.navigation.page import StreamlitPage

from functools import partial
from typing import Callable, get_args
from types import ModuleType

from book.pages import page_week_01, page_week_02, page_week_03, page_week_04
from book.common import page_config_common, apply_css_style, sidebar_common


def generate_list_of_pages(page_week: Callable, nweek: int) -> list[StreamlitPage]:
    list_of_topics = get_args(page_week.__annotations__["option"])

    pages = []

    for i, topic in enumerate(list_of_topics, start=1):
        if not topic.startswith("~"):
            pages.append(
                st.Page(
                    partial(page_week, topic),
                    title=(title := f"{topic}"),
                    url_path=title.replace(" ", "_"),
                    icon=":material/article:"
                )
            )

        else:
            pages.append(
                st.Page(
                    partial(page_week, topic),
                    title=(title := " - " + topic.replace("~", "")),
                    url_path=title.replace(" ", "_"),
                    icon="🐍",
                )
            )

    return pages


def generate_list_sidequest_pages(subpage: ModuleType):
    subpage.__all__


def entrypoint_page():
    st.title("Hydraulics with Python")

    "Hehe :violet[magic]"


def main():
    st.set_page_config(**page_config_common)
    apply_css_style()
    sidebar_common()

    entry_page = st.Page(entrypoint_page, title="Cover", default=True, icon=":material/book_2:")

    nav = st.navigation(
        {
            "Main": [entry_page],
            "Week 1": generate_list_of_pages(page_week_01, 1),
            "Week 2": generate_list_of_pages(page_week_02, 2),
            "Week 3": generate_list_of_pages(page_week_03, 3),
            "Week 4": generate_list_of_pages(page_week_04, 4),
        }
    )

    nav.run()


if __name__ == "__main__":
    main()
