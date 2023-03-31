import streamlit as st
from stpyvista import stpyvista
import matplotlib.pyplot as plt
import pyvista as pv
import pickle, json
import numpy as np
from pathlib import Path

def main():
    
    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)
    
    #####################################################################

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"
    
    "## Centifugal pump"

    file = Path("assets/3d/pump.STL")
    reader = pv.STLReader(file)
    mesh = reader.read()
    
    axes = pv.Axes(show_actor=True, actor_scale=2.0, line_width=5)
    axes.origin = (0,0,0)
    rotated = mesh.rotate_x(90.0, point=axes.origin, inplace=False)
    
    plotter = pv.Plotter(border=False, window_size=[700,600]) 
    plotter.background_color = "#dddddd"
    # plotter.add_mesh(mesh, color="salmon")
    plotter.add_mesh(
        rotated, 
        color='lightgrey',
        pbr=False, 
    )

    plotter.view_isometric()

    url = "https://www.3dcontentcentral.com/secure/download-model.aspx?catalogid=171&id=118829"
    st.caption(f"Source: [3dcontentcentral]({url})")
    stpyvista(plotter, key="st_pump")

if __name__ == "__main__":
    main()