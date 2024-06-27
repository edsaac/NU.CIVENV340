import streamlit as st
from streamlit.navigation.page import StreamlitPage
from functools import partial
from typing import Callable, get_args

from book.week_01.Week_1 import page_week_01
from book.week_02.Week_2 import page_week_02
from book.week_03.Week_3 import page_week_03
from book.week_04.Week_4 import page_week_04
from book.week_05.Week_5 import page_week_05
from book.week_06.Week_6 import page_week_06
from book.week_07.Week_7 import page_week_07
from book.week_08.Week_8 import page_week_08
from book.week_09.Week_9 import page_week_09
from book.week_10.Week_10 import page_week_10
from book.extra import appendices

__all__ = ["all_pages"]

all_sections = {
    "Week 1 - Basics & introduction": page_week_01,
    "Week 2 - Head losses": page_week_02,
    "Week 3 - Pipe networks": page_week_03,
    "Week 4 - Pumps": page_week_04,
    "Week 5 - Open-channel flow": page_week_05,
    "Week 6 - More channel flow": page_week_06,
    "Week 7 - Hydraulic structures": page_week_07,
    "Week 8 - Watersheds and water cycle": page_week_08,
    "Week 9 - Hydrology and engineering": page_week_09,
    "Week 10 - Basics of probability": page_week_10,
    "Appendices": appendices,
}


def generate_pages(page_week: Callable) -> dict[str, StreamlitPage]:
    list_of_topics = get_args(page_week.__annotations__["option"])

    pages = {}

    for i, topic in enumerate(list_of_topics, start=1):
        if not topic.startswith("~"):
            pages[topic] = st.Page(
                partial(page_week, topic),
                title=(title := f"{topic}"),
                url_path=title.replace(" ", "_").replace("-", "").strip().lower(),
                icon=":material/article:",
            )

        else:
            pages[topic] = st.Page(
                partial(page_week, topic),
                title=(title := " - " + topic.replace("~", "")),
                url_path=title.replace("-", "").strip().replace(" ", "_").lower(),
                icon="🐍",
            )

    return pages


all_pages = {"Cover": None}

for section_title, page_callable in all_sections.items():
    all_pages[section_title] = generate_pages(page_callable)
