import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pickle
import numpy as np
from statistics import mean

from pysheds.grid import Grid
import rasterio

from streamlit_folium import st_folium
import folium

from collections import namedtuple
Point = namedtuple("Point", ['x','y'])

DIRMAP = (64, 128, 1, 2, 4, 8, 16, 32) # (D8 for mapping) <- This should be a categorical map

def main():

    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    file_location = "assets/dem/clipped.tif"

    # with st.expander("DEM details"):
    #     import subprocess
    #     subprocess.check_output(["gdalinfo", file_location]).decode('utf-8')

    with rasterio.open(file_location) as src:

        bottom, top = src.bounds.bottom, src.bounds.top
        left, right = src.bounds.left, src.bounds.right


        from rasterio.enums import Resampling
        upscale_factor = 0.10
        
        downscaled_data = src.read(
            out_shape=(
                src.count,
                int(src.height * upscale_factor),
                int(src.width * upscale_factor)
            ),
            resampling=Resampling.bilinear
        )

        # scale image transform
        transform = src.transform * src.transform.scale(
            (src.width / downscaled_data.shape[-1]),
            (src.height / downscaled_data.shape[-2])
        )

        
    with st.sidebar:

        tiles = st.selectbox(
            "🌌 Pick a map style:", 
            [
                "OpenStreetMap", 
                "Stamen Terrain", 
                "Stamen Toner", 
                "Stamen Watercolor", 
                "CartoDB Positron", 
                "CartoDB Dark_Matter"
            ], 
            index=2)
        
        st.markdown(fr"""
        *****
        ## ℹ️ Source:

        Bartos, M., (2020) <br>
        `pysheds` *simple and fast watershed delineation in python*.<br>
        DOI: [10.5281/zenodo.3822494](https://doi.org/10.5281/zenodo.3822494)
        Check the [repository here](https://github.com/mdbartos/pysheds).
        """, unsafe_allow_html=True)


        rf"""
        ## 🖼️ DEM properties
        
        **Size:** $ \; {src.width} \times {src.height} \mathrm{{px}}$

        **Bounds:**
        
        $$
        \begin{{array}}{{rrcr}}
            \textsf{{W:}} & {src.bounds.left:.2f}\degree &\to& {src.bounds.right:.2f}\degree \\
            \textsf{{N:}} & {src.bounds.bottom:.2f}\degree &\to& {src.bounds.top:.2f}\degree
        \end{{array}}
        $$
        """

    ####################################
    ### Page layout
    ####################################
    map_container = st.empty()
    dem_container = st.empty()
    network_container = st.empty()
    flow_container = st.empty()
    delineated_container = st.empty()
    distance_container = st.empty()

    ####################################
    ### Processing
    ####################################

    # Specify pour point
    with st.sidebar:
        "******"
        def reset_maps_catchment():
            del st.session_state.maps_catchment

        with st.form("Pour point location"):
            "### Pour point location"
            cols = st.columns(2)
            with cols[0]: 
                y = st.number_input(
                    "Latitude", 
                    bottom, top, 33.1032, 0.1, 
                    format="%.3f",
                    help="Latitude of the pour point for basin delimitation, e.g., 33.805"
                )

            with cols[1]: 
                x = st.number_input(
                    "Longitude", 
                    left, right, -83.7943, 0.1, 
                    format="%.3f",
                    help="Longitude of the pour point for basin delimitation, e.g., -84.500"
                )
            
            pour_point = (x,y)

            st.form_submit_button("Submit", use_container_width=True, on_click=reset_maps_catchment)

    if "maps" not in st.session_state:
        st.session_state.maps = dict()
        
        #- Follow pysheds workflow
        # Read elevation raster   
        grid = Grid.from_raster(file_location)
        st.session_state.maps["grid"] = grid

        dem = grid.read_raster(file_location)
        st.session_state.maps["dem"] = dem

        # Fill pits and depressions in DEM
        pit_filled_dem = grid.fill_pits(dem)
        flooded_dem = grid.fill_depressions(pit_filled_dem)

        # Resolve flats in DEM
        inflated_dem = grid.resolve_flats(flooded_dem)

        # Compute flow directions
        fdir = grid.flowdir(inflated_dem, dirmap=DIRMAP)
        st.session_state.maps["fdir"] = fdir

        # Calculate flow accumulation
        acc = grid.accumulation(fdir, dirmap=DIRMAP)
        st.session_state.maps["acc"] = acc
        
    else: 
        grid = st.session_state.maps["grid"]
        dem = st.session_state.maps["dem"]
        acc = st.session_state.maps["acc"]
        fdir = st.session_state.maps["fdir"]

    ####################################
    ### Contents // Static
    ####################################
    with map_container.container():
        "### General location"
        midpoint = Point(mean([bottom, top]),mean([left,right]))
        m = folium.Map(location=midpoint, zoom_start=8, tiles=tiles)
        boundary = [(bottom, left), (bottom,right), (top, right), (top,left), (bottom,left)]
        folium.Polygon(boundary, tooltip="DEM boundary").add_to(m)
        folium.Marker((pour_point[1], pour_point[0]), tooltip="Pour point (Outlet)", icon=folium.Icon("purple")).add_to(m)
        st_folium(m, width=600, height=500, returned_objects=[])
        
    with dem_container.container():
        r"""
        ****
        ### DEM: Digital Elevation Model
        """
        tabs = st.tabs(["Heatmap", "Hillshade", "Contours"])
        with tabs[0]: 
            st.pyplot(plot_map(dem, grid))
        with tabs[1]: 
            st.pyplot(plot_hillshade(dem, grid))
        with tabs[2]:
            # st.pyplot(plot_contours(dem, grid))
            st.pyplot(plot_contours(downscaled_data[0], grid))

    with flow_container.container():
        r"""
        *****
        ### Flow accumulation
        """
        st.pyplot(plot_accumulation(acc, grid))  

    if "maps_catchment" not in st.session_state:
        st.session_state.maps_catchment = dict()
        
        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 1000, pour_point)

        # Delineate the catchment
        catch = grid.catchment(
            x=x_snap, 
            y=y_snap, 
            fdir=fdir, 
            dirmap=DIRMAP, 
            xytype='coordinate'
        )

        # Clip the bounding box to the catchment
        # grid.clip_to(catch)
        clipped_catch = grid.view(catch)
        st.session_state.maps_catchment["clipped_catch"] = clipped_catch
        
        # Extract river network
        branches = grid.extract_river_network(fdir, acc > 1000, dirmap=DIRMAP)
        st.session_state.maps_catchment["branches"] = branches

        # Calculate distance to outlet from each cell
        dist = grid.distance_to_outlet(
            x=x_snap, 
            y=y_snap, 
            fdir=fdir, 
            dirmap=DIRMAP,
            xytype='coordinate')
        
        st.session_state.maps_catchment["dist"] = dist

    else: 
        clipped_catch = st.session_state.maps_catchment["clipped_catch"]
        branches = st.session_state.maps_catchment["branches"]
        dist = st.session_state.maps_catchment["dist"]

    ####################################
    ### Contents // Dynamic
    ####################################

    with network_container.container():
        r"""
        *****
        ### Flow direction

        **D8 algorithm:**
        """
        cols = st.columns(2)
        with cols[0]:
            st.markdown(
                r"""
                <style type="text/css">
                .tg  {border-collapse:collapse;border-spacing:0;margin:0px auto;}
                .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                overflow:hidden;padding:10px 5px;word-break:normal;}
                .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
                .tg .tg-amwm{font-weight:bold;text-align:center;vertical-align:top}
                </style>
                <table class="tg" style="undefined;table-layout: fixed; width: 153px">
                <colgroup>
                <col style="width: 51px">
                <col style="width: 51px">
                <col style="width: 51px">
                </colgroup>
                <tbody>
                <tr>
                    <td class="tg-amwm">NW</td>
                    <td class="tg-amwm">N</td>
                    <td class="tg-amwm">NE</td>
                </tr>
                <tr>
                    <td class="tg-amwm">W</td>
                    <td class="tg-amwm"></td>
                    <td class="tg-amwm">E</td>
                </tr>
                <tr>
                    <td class="tg-amwm">SW</td>
                    <td class="tg-amwm">S</td>
                    <td class="tg-amwm">SE</td>
                </tr>
                </tbody>
                </table>
                """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(
                r"""
                <style type="text/css">
                .tg  {border-collapse:collapse;border-spacing:0;margin:0px auto;}
                .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                overflow:hidden;padding:10px 5px;word-break:normal;}
                .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
                .tg .tg-amwm{font-weight:bold;text-align:center;vertical-align:top}
                </style>
                <table class="tg" style="undefined;table-layout: fixed; width: 153px">
                <colgroup>
                <col style="width: 51px">
                <col style="width: 51px">
                <col style="width: 51px">
                </colgroup>
                <tbody>
                <tr>
                    <td class="tg-amwm">32</td>
                    <td class="tg-amwm">64</td>
                    <td class="tg-amwm">128</td>
                </tr>
                <tr>
                    <td class="tg-amwm">16</td>
                    <td class="tg-amwm"></td>
                    <td class="tg-amwm">1</td>
                </tr>
                <tr>
                    <td class="tg-amwm">8</td>
                    <td class="tg-amwm">4</td>
                    <td class="tg-amwm">2</td>
                </tr>
                </tbody>
                </table>
                """, unsafe_allow_html=True
            )

        "&nbsp;"

        st.pyplot(plot_network(branches, grid, pour_point))

    with delineated_container.container():
        rf"""
        ****
        ### Delineated catchment
        
        Pour point coordinates: {pour_point[1]}° N, {pour_point[0]}° W
        """
        st.pyplot(plot_catchment(clipped_catch, dem, grid, pour_point))

    with distance_container.container():
        r"""
        *****
        ### Distance to pour point
        """
        st.pyplot(plot_distance(dist, grid))



@st.cache_data
def plot_map(_dem, _grid):
    fig, ax = plt.subplots(figsize=(8,6))

    img = ax.imshow(_dem, extent=_grid.extent, cmap='terrain', zorder=1)
    fig.colorbar(img, label='Elevation (m)', shrink=0.5)
    ax.grid(zorder=0)
    ax.set_title('Digital elevation map (Heatmap)', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect("equal")
    fig.set_tight_layout(True)
    return fig

@st.cache_data
def plot_hillshade(_dem, _grid):

    from matplotlib.colors import LightSource
    ls = LightSource(azdeg=315, altdeg=45)
    
    fig, ax = plt.subplots(figsize=(8,6))
    ax.imshow(
        ls.hillshade(_dem, vert_exag=0.5, dx=1.0, dy=1.0), 
        extent=_grid.extent, cmap='gray'
    )
    
    ax.grid(True, zorder=0, c="pink")
    ax.set_title('Digital elevation map (Hillshade)', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect("equal")
    fig.set_tight_layout(True)
    return fig

def plot_contours(_dem, _grid):

    fig, ax = plt.subplots(figsize=(8,6))

    csf = ax.contourf(
        np.flipud(_dem), 
        extent=_grid.extent, 
        levels = np.arange(50,400,50), 
        cmap="Greens_r",
    )

    fig.colorbar(csf, label='Elevation (m)', shrink=0.5)
    
    cs = ax.contour(
        np.flipud(_dem), 
        extent=_grid.extent, 
        levels = np.arange(100,550,50), 
        colors="k", 
        linewidths=1
    )

    ax.clabel(
        cs, 
        levels=np.arange(100,550,100), 
        inline=True,
        fontsize=12
    )

    
    #img = ax.imshow(_dem, extent=_grid.extent, cmap='Greys', zorder=1)

    ax.grid(zorder=0)
    ax.set_title('Digital elevation map (Contours)', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect("equal")
    fig.set_tight_layout(True)
    return fig


@st.cache_data
def plot_accumulation(_acc, _grid):
    from matplotlib.colors import LogNorm
    
    fig, ax = plt.subplots(figsize=(8,6))
    img = ax.imshow(_acc, extent=_grid.extent, zorder=2,
                cmap='cubehelix',
                norm=LogNorm(1, _acc.max()),
                interpolation='bilinear')
    fig.colorbar(img, ax=ax, label='Upstream Cells', shrink=0.5)
    ax.grid(True, zorder=0)
    ax.set_title('Flow Accumulation', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect("equal")
    fig.set_tight_layout(True)
    return fig

@st.cache_data
def plot_catchment(_clip, _dem, _grid, pour_point):
    
    fig, ax = plt.subplots(figsize=(8,6))
    
    img = ax.imshow(
        np.where(_clip, _clip, np.nan), 
        zorder=2, alpha=0.2,
        cmap='Greys_r', extent=_grid.extent
    )

    img = ax.imshow(_dem, alpha=0.95, cmap='terrain', zorder=0, extent=_grid.extent)
    fig.colorbar(img, ax=ax, label='Elevation (m)', shrink=0.5)

    ax.add_artist(
        Circle(pour_point, 0.02, fc="purple", zorder=4)
    )

    ax.grid('on', zorder=0)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Delineated Catchment', size=14)
    ax.set_aspect("equal")
    return fig

@st.cache_data
def plot_network(_branches, _grid, pour_point):
    fig, ax = plt.subplots(figsize=(8,6))

    for branch in _branches['features']:
        line = np.asarray(branch['geometry']['coordinates'])
        plt.plot(line[:, 0], line[:, 1], c="k", lw=0.2)

    ax.add_artist(
        Circle(pour_point, 0.02, fc="purple", zorder=4)
    )

    ax.grid(True, zorder=0)
    ax.set_xlim(_grid.bbox[0], _grid.bbox[2])
    ax.set_ylim(_grid.bbox[1], _grid.bbox[3])
    ax.set_title('D8 channels', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')
    return fig

@st.cache_data
def plot_distance(dist, _grid):
    fig, ax = plt.subplots(figsize=(8,6))
    img = ax.imshow(dist, extent=_grid.extent, zorder=2, cmap='cubehelix_r')
    fig.colorbar(img, ax=ax, label='Distance to outlet (cells)', shrink=0.5)
    ax.grid(True, zorder=0)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Flow Distance', size=14)
    ax.set_aspect("equal")
    return fig

if __name__ == "__main__":
    main()

#st.map()

# with rasterio.open(file_location) as src:
#     z = src.read()

#     with st.sidebar:
#         st.metric("Dimensions", f"{src.width} x {src.height}")
#         st.metric("EW-Bounds", f"{src.bounds.left:.2f} ↔ {src.bounds.right:.2f}")
#         st.metric("NS-Bounds", f"{src.bounds.bottom:.2f} ↔ {src.bounds.top:.2f}")
#         st.metric("CRS", f"{src.crs}")
#         st.metric("Bands", f"{src.count}")

# fig, ax = plt.subplots()
# ax.imshow(z[0])
# st.pyplot(fig)

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
# ax.imshow(z[0])

# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.STATES, linestyle=':')
# ax.add_feature(cfeature.LAKES, alpha=0.5)
# ax.add_feature(cfeature.RIVERS)
# ax.set_extent([-84, -82, 32, 34.5], crs=ccrs.PlateCarree())

# st.pyplot(fig)