import streamlit as st
from pysheds.grid import Grid
from pathlib import Path
import rasterio
import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import subprocess
from streamlit_folium import st_folium
import folium
from statistics import mean
import pickle
import numpy as np

from collections import namedtuple
Point = namedtuple("Point", ['x','y'])

def main():

    with open("assets/page_config.pkl", 'rb') as f:
        st.session_state.page_config = pickle.load(f)
    
    st.set_page_config(**st.session_state.page_config)

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    # options = [
    #     "assets/.ignore/n30w090_dem/clipped.tif",
    #     "assets/.ignore/elevation.tiff",
    #     "assets/.ignore/n30w090_dem/n30w090_dem.tif",
    # ]

    # file_location = st.selectbox("Option", options)
    file_location = "assets/dem/clipped.tif"

    # with st.expander("DEM details"):
    #     subprocess.check_output(["gdalinfo", file_location]).decode('utf-8')

    with rasterio.open(file_location) as src:
        bottom, top = src.bounds.bottom, src.bounds.top
        left, right = src.bounds.left, src.bounds.right
        
    with st.sidebar:
        #CITE pysheds
        fr"""
        ## Source:

        This example is using [`pysheds`](https://doi.org/10.5281/zenodo.3822494): 
        *simple and fast watershed delineation in python*, from 
        Bartos, M., 2020. 
        
        Check the [repository](https://github.com/mdbartos/pysheds).

        *****
        """

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

        rf"""
        *****
        ### DEM dimensions
        
        **Size:**
        
        $$
            {src.width} \times {src.height} \mathrm{{px}}
        $$
        """

        rf"""
        **Bounds:**
        
        East:

        $$
            \begin{{array}}{{rcl}}
                {src.bounds.left:.2f}\degree \longleftrightarrow {src.bounds.right:.2f}\degree
            \end{{array}}
        $$
        """

        r"""
        # North:

        # $$
        #     \begin{{array}}{{rcl}}
        #         {src.bounds.bottom:.2f}\degree \longleftrightarrow {src.bounds.top:.2f}\degree
        #     \end{{array}}
        # $$

        # """

    ## Layout
    map_container = st.empty()
    dem_container = st.empty()
    flow_container = st.empty()
    delineated_container = st.empty()

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
        dirmap = (64, 128, 1, 2, 4, 8, 16, 32) # (D8 for mapping) <- This should be a categorical map
        fdir = grid.flowdir(inflated_dem, dirmap=dirmap)

        # Calculate flow accumulation
        acc = grid.accumulation(fdir, dirmap=dirmap)
        st.session_state.maps["acc"] = acc


        # Specify pour point
        y, x = 33.1032,-83.7943

        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 1000, (x, y))

        # Delineate the catchment
        catch = grid.catchment(
            x=x_snap, 
            y=y_snap, 
            fdir=fdir, 
            dirmap=dirmap, 
            xytype='coordinate'
        )

        # Clip the bounding box to the catchment
        # grid.clip_to(catch)
        clipped_catch = grid.view(catch)
        
            
        # Extract river network
        branches = grid.extract_river_network(fdir, acc > 50, dirmap=dirmap)
        #st.pyplot(plot_network(branches, grid))

        # Calculate distance to outlet from each cell
        dist = grid.distance_to_outlet(
            x=x_snap, 
            y=y_snap, 
            fdir=fdir, 
            dirmap=dirmap,
            xytype='coordinate')
        
        # st.pyplot(plot_distance(dist, grid))

    else: 
        grid = st.session_state.maps["grid"]
        dem = st.session_state.maps["dem"]
        acc = st.session_state.maps["acc"]

    st.write(dem)

    with st.sidebar:
        "******"
        st.metric("Shape", f"{dem.shape}")
        st.metric("NoData", f"{dem.nodata}")
        st.code(f"CRS: {dem.crs}")

    with map_container.container():
        "### General location"
        midpoint = Point(mean([bottom, top]),mean([left,right]))
        m = folium.Map(location=midpoint, zoom_start=8, tiles=tiles)
        boundary = [(bottom, left), (bottom,right), (top, right), (top,left), (bottom,left)]
        folium.PolyLine(boundary, tooltip="DEM boundary").add_to(m)
        st_folium(m, width=800, height=700, returned_objects=[])
        
    with dem_container.container():
        "### DEM"
        tabs = st.tabs(["Heatmap", "Hillshade", "Contours"])
        with tabs[0]: 
            st.pyplot(plot_map(dem, grid))
        with tabs[1]: 
            st.pyplot(plot_hillshade(dem, grid))
        with tabs[2]:
            st.pyplot(plot_contours(dem, grid))

    with flow_container.container():
        "### Flow accumulation"
        st.pyplot(plot_accumulation(acc, grid))    

    with delineated_container.container():
        "### Delineated catchment"
        st.pyplot(plot_catchment(clipped_catch, dem, grid))
        


@st.cache_data
def plot_map(_dem, _grid):
    fig, ax = plt.subplots(figsize=(8,6))
    fig.patch.set_alpha(0)

    img = ax.imshow(_dem, extent=_grid.extent, cmap='terrain', zorder=1)
    fig.colorbar(img, label='Elevation (m)', shrink=0.5)
    ax.grid(zorder=0)
    ax.set_title('Digital elevation map', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
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
    
    ax.grid(True, zorder=0)
    ax.set_title('Digital elevation map (Hillshade)', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    fig.set_tight_layout(True)
    return fig

def plot_contours(_dem, _grid):
    fig, ax = plt.subplots(figsize=(8,6))

    cs = ax.contour(np.flipud(_dem), extent=_grid.extent, levels = [80], colors="r", linewidths=1)
    ax.clabel(cs, inline=True)
    
    img = ax.imshow(_dem, extent=_grid.extent, cmap='Greys', zorder=1)

    ax.grid(zorder=0)
    ax.set_title('Digital elevation map', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
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
    fig.set_tight_layout(True)
    return fig


def plot_catchment(clipped_catch, dem, grid):
    
    fig, ax = plt.subplots(figsize=(8,6))
    
    img = ax.imshow(
        np.where(clipped_catch, clipped_catch, np.nan), 
        zorder=2, alpha=0.3,
        cmap='Greys_r', extent=grid.extent
    )

    img = ax.imshow(dem, cmap='terrain', zorder=0, extent=grid.extent)
    fig.colorbar(img, ax=ax, label='Catchment', shrink=0.5)
    ax.grid('on', zorder=0)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Delineated Catchment', size=14)
    return fig

def plot_network(branches, grid):
    fig, ax = plt.subplots(figsize=(8,6))


    for branch in branches['features']:
        line = np.asarray(branch['geometry']['coordinates'])
        plt.plot(line[:, 0], line[:, 1], c="k", lw=0.2)
    
    ax.grid(True, zorder=0)
    ax.set_xlim(grid.bbox[0], grid.bbox[2])
    ax.set_ylim(grid.bbox[1], grid.bbox[3])
    ax.set_title('D8 channels', size=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')
    return fig

def plot_distance(dist, grid):
    fig, ax = plt.subplots(figsize=(8,6))
    img = ax.imshow(dist, extent=grid.extent, zorder=2, cmap='cubehelix_r')
    fig.colorbar(img, ax=ax, label='Distance to outlet (cells)', shrink=0.5)
    ax.grid(True, zorder=0)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Flow Distance', size=14)
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