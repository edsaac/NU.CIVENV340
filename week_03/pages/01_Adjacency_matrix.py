import streamlit as st

def main():

    st.set_page_config(layout='wide')

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    #####################################################################

    "## Adjacency matrix"
    st.components.v1.iframe("https://mathworld.wolfram.com/AdjacencyMatrix.html", width=600, height=700, scrolling=True)

if __name__ == "__main__":
    main()