import streamlit as st
import pickle

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    with st.sidebar:
        lottie = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_tuzu65Bu6N.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 150px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=150)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "System curve", 
                "Types of pumps", 
                "Characteristic curves", 
                "Cavitation", 
                "Pumps in series/parallel"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441]) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
        Pearson Education Inc., Boston.
        """
    
        cols = st.columns(2)
        with cols[0]:
            r"""
            [![Github Repo](https://img.shields.io/static/v1?label=&message=Repository&color=black&logo=github)](https://github.com/edsaac/NU.CIVENV340)
            """
        with cols[1]:
            r""" [![Other stuff](https://img.shields.io/static/v1?label=&message=Other+stuff&color=white&logo=streamlit)](https://edsaac.github.io)"""
    
    ####################################################################
    
    if option == "System curve":
        r" ### 🚧 Under construction 🚧"

    elif option == "Types of pumps":
        r" ### 🚧 Under construction 🚧"

    elif option == "Characteristic curves":
        r" ### 🚧 Under construction 🚧"

    elif option == "Cavitation":
        r" ### 🚧 Under construction 🚧"

    elif option == "Pumps in series/parallel":
        r" ### 🚧 Under construction 🚧"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

if __name__ == "__main__":
    main()