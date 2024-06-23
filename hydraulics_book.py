import streamlit as st
from streamlit.navigation.page import StreamlitPage

from functools import partial
from typing import Callable, get_args

from week_01.Week_1 import page_week_01
from week_02.Week_2 import page_week_02
from week_03.Week_3 import page_week_03

def generate_list_of_pages(page_week: Callable, week_number: int) -> list[StreamlitPage]:
    list_of_topics = get_args(page_week.__annotations__["option"])
    
    return [
        st.Page(
            partial(page_week, topic), 
            title=(title:=f"{week_number}.{i} - {topic}"), 
            url_path=title.lower()
        )
        for i, topic in enumerate(list_of_topics, start=1)
    ]


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
                """[![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""
            )

def entrypoint_page():
    st.title("Hydraulics with Python")


def main():
    entry_page = st.Page(entrypoint_page, title="**Book**")

    nav = st.navigation(
        {
            "Main": [entry_page],
            "Week 1": generate_list_of_pages(page_week_01, 1),
            "Week 2": generate_list_of_pages(page_week_02, 2),
            "Week 3": generate_list_of_pages(page_week_03, 3),

        }
    )

    nav.run()


if __name__ == "__main__":
    main()
