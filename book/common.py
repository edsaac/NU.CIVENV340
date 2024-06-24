import streamlit as st
import requests
from base64 import b64encode
from PIL import Image
from io import BytesIO

__all__ = [
    "sidebar_common",
    "page_config_common",
    "axis_format",
    "apply_css_style",
    "get_pdf_as_bytes",
    "get_image_as_bytes",
    "get_image_as_PIL",

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
                """
                [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)
                """
            )


page_config_common = dict(
    layout="wide",
    menu_items={
        "Get help": "https://canvas.northwestern.edu/courses/189865",
        "Report a bug": "https://github.com/edsaac/NU.CIVENV340/issues/new",
        "About": R"""
            **CIVENV 340: Hydraulics & Hydrology** - Supporting material

            - Northwestern University - Spring/2023
            - Instructor: Edwin Saavedra Cifuentes

            [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff+from+Edwin&color=white&logo=streamlit)](https://edsaac.github.io)
            
            *****
            """,
    },
)

axis_format = dict(
    title_font_size=20,
    tickfont_size=16,
    showline=True,
    color="RGBA(1, 135, 73, 0.3)",
    tickcolor="RGBA(1, 135, 73, 0.3)",
    showgrid=True,
    griddash="dash",
    linewidth=1,
    gridcolor="RGBA(1, 135, 73, 0.3)",
)


@st.cache_resource
def _css_stylesheet(path: str = "./book/assets/style.css"):
    with open(path) as f:
        css = f.read()

    return css


def apply_css_style():
    css = _css_stylesheet()
    st.html(f"<style> {css} </style>")


@st.cache_resource
def get_pdf_as_bytes(url: str):
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        return b64encode(r.content).decode("utf-8")


_headers_for_request = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Priority": "u=1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


@st.cache_resource
def get_image_as_bytes(url: str):
    r = requests.get(url, stream=True, headers=_headers_for_request)

    if r.status_code == requests.codes.ok:
        return r.content

    else:
        raise requests.HTTPError("Request failed " f"{r.status_code = }")


@st.cache_resource
def get_image_as_PIL(url: str):
    bytes_img = get_image_as_bytes(url)
    return Image.open(BytesIO(bytes_img), formats=["png", "jpg"])
