import streamlit as st
from stpyvista import stpyvista
from stpyvista.utils import start_xvfb
import pyvista as pv


def pump_render():
    st.header("Centifugal pump")
    start_xvfb()

    file = "./book/assets/3d/pump.STL"
    reader = pv.STLReader(file)
    mesh = reader.read()

    axes = pv.Axes(show_actor=True, actor_scale=2.0, line_width=5)
    axes.origin = (0, 0, 0)
    rotated = mesh.rotate_x(90.0, point=axes.origin, inplace=False)

    plotter = pv.Plotter(border=False, window_size=[700, 600])
    plotter.background_color = "#dddddd"
    # plotter.add_mesh(mesh, color="salmon")
    plotter.add_mesh(
        rotated,
        color="lightgrey",
        pbr=False,
    )

    plotter.view_isometric()

    url = "https://www.3dcontentcentral.com/secure/download-model.aspx?catalogid=171&id=118829"
    st.caption(f"Source: [3dcontentcentral]({url})")
    stpyvista(plotter, key="st_pump")


if __name__ == "__main__":
    pump_render()
