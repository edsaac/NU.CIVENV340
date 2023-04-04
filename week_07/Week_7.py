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
        <lottie-player src="https://assets4.lottiefiles.com/private_files/lf30_nep75hmm.json"  background="transparent"  speed="1.5"  style="width: 200px; height: 100px;"  loop  autoplay></lottie-player>
        """
        st.components.v1.html(lottie, width=200, height=100)

        "### Select a topic:"
        option = st.radio("Select a topic:",
            [
                "Non-erodible channels",
                "Unlined channel design",
                "Flow measurement devices [Pipes]",
                "Flow measurement devices [Channels]"
            ],
            label_visibility="collapsed")
        
        "***"
        st.image("https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.php?client=primo&isbn=9780134292380/sc.jpg")
        
        r"""
        #### Class textbook:
        [🌐](https://search.library.northwestern.edu/permalink/01NWU_INST/h04e76/alma9980502032702441) *Houghtalen, Akan & Hwang* (2017). **Fundamentals of hydraulic engineering systems** 5th ed.,
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
    
    if option == "Non-erodible channels":
        r""" 
        ## Non-erodible channels

        Factors to consider:
        
        ### Efficient hydraulic section
            - Geometric conditions that minimize the wetter perimeter
        
        - Practicability
        - Cost

        ### Minimum permisible velocity:
            - Lowest velocity that will not result in sedimentation or induce
            vegetation growth

        ### Channel Slopes
        """

    if option == "Unlined channel design":
        r""" 
        ## Non-erodible channels

        Factors to consider:
        
        ### Efficient hydraulic section
            - Geometric conditions that minimize the wetter perimeter
        
        - Practicability
        - Cost

        ### Minimum permisible velocity:
            - Lowest velocity that will not result in sedimentation or induce
            vegetation growth

        ### Channel side slopes
            - Maximum stable slope depending on the material

        ### Freeboard
        
        $$
            F = \sqrt{C\,y}
        $$
        """

    else: 
        st.error("You should not be here!")
        r"""
        ## Unlined channel

        ### Maximum permissible velocity
        
        1. Select material: ($n$, $m$ and $V_{\rm max})
        2. Calculate the hydraulic radius 
        3. Given a discharge, calculate the cross-sectional area
        4. Calculate the wetted perimeter
        5. Solve for depth $y$ and bottom width $b$
        6. Adjust dimensions and add a freeboard 

        ### Tractive force


        *********
        ### Grass channels

        #### Design for stability

        #### Modification for conveyance

        """

if __name__ == "__main__":
    main()