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
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ntrhqntu.json"  background="transparent"  speed="1.5"  style="width: 260px; height: 250px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=250, height=250)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [   
                "Transitions and jumps",
                "Energy losses",
                "Uniform flow",
                "Gradually varied flow", 
                "Water profiles",
                "Free-surface calculation",
                "Sediments & rivers",
                "Lane's diagram",
                "Shear stress"
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
    
    if option == "Transitions and jumps":
        r"### 🚧 Under construction 🚧"
    elif option == "Energy losses":
        r"### 🚧 Under construction 🚧"
    elif option == "Uniform flow":
        r"### 🚧 Under construction 🚧"
    elif option == "Gradually varied flow":
        r"### 🚧 Under construction 🚧"
    elif option == "Water profiles":
        r"### 🚧 Under construction 🚧"
    elif option == "Free-surface calculation":
        r"### 🚧 Under construction 🚧"
    elif option == "Sediments & rivers":
        r"### 🚧 Under construction 🚧"
    elif option == "Lane's diagram":
        r"### 🚧 Under construction 🚧"
    elif option == "Shear stress":
        r"### 🚧 Under construction 🚧"

    else: 
        st.error("You should not be here!")
        r" ### 🚧 Under construction 🚧"

if __name__ == "__main__":
    main()