import streamlit as st
import plotly.graph_objects as go
from itertools import cycle
import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def main(): 
    st.set_page_config(layout='wide')

    with open("assets/style.css") as f:
        st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

    st.title("CIV-ENV 340: Hydraulics and hydrology")
    "****"

    #####################################################################

    f_cw = cw_multidimensional()
    f_sj = sj_multidimensional()
    
    cols = st.columns(2)
    with cols[0]:
        "#### Colebrook-White eq."
        st.pyplot(friction_factor_heatmap(f_cw))
    
    with cols[1]:
        "#### Swamme-Jain eq."
        st.pyplot(friction_factor_heatmap(f_sj))

    "#### Difference between the two equations"
    
    cols = st.columns([1,2,1])
    with cols[1]:
        st.pyplot(error_equations_heatmap())

NCELLS = 30
Re = np.logspace(4, 8, NCELLS, base=10.0)
eD = np.logspace(-6, -1, NCELLS, base=10)

def friction_factor_heatmap(fzz):
    fig,ax = plt.subplots(figsize=(5,6))
    cont = ax.contour(Re, eD, fzz, levels=10, colors="k", linewidths=np.linspace(0.1,2,10))
    ax.clabel(cont, cont.levels[0:2], inline=True, fontsize=8, inline_spacing=105, manual=[(5e7, 3e-5)])
    #ax.clabel(cont, cont.levels[2:5], inline=True, fontsize=8, inline_spacing=2, manual=[(1e7,1e-3), (1e7, 1e-3), (5e6, 9e-3)])

    im = ax.pcolormesh(Re, eD, fzz, vmin=0.007, vmax=0.10, cmap='bone_r')
    plt.colorbar(im, shrink=0.5, label="Friction factor $f$", orientation='horizontal', location='top')
    ax.set_xlabel(r"Reynolds number -- $R_e$")
    ax.set_ylabel(r"Relative pipe roughness -- $e/D$")
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig

def cw_root(f:float, rel_roughness:float, reynolds_number:float):
    return f - 1.0 / np.power(- 2.0 * np.log10(rel_roughness/3.7 + 2.51/(reynolds_number*np.sqrt(f))), 2)

def swamme_jain(relative_roughness:float, reynolds_number:float):
    fcalc = 0.25 / np.power(np.log10(relative_roughness/3.7 + 5.74/np.power(reynolds_number, 0.9)), 2)
    return fcalc

@st.cache_data
def cw_multidimensional():
    Rexx, eDyy = np.meshgrid(Re, eD)
    init_f = 0.05 * np.ones_like(Rexx)
    sol = root(cw_root, init_f, args=(eDyy.flatten(), Rexx.flatten()))
    fzz = sol.x.reshape(NCELLS, NCELLS)
    return fzz

@st.cache_data
def sj_multidimensional():
    Re = np.logspace(4, 8, NCELLS, base=10.0)
    eD = np.logspace(-6, -1, NCELLS, base=10)
    Rexx, eDyy = np.meshgrid(Re, eD)
    fzz = swamme_jain(eDyy, Rexx)
    return fzz

def error_equations_heatmap():
    f_sj = sj_multidimensional()
    f_cw = cw_multidimensional()

    r"""
    $$
        \textsf{Percent error} = \dfrac{f_{\rm SJ} - f_{\rm CW}}{f_{\rm CW}}
    $$
    """

    fig, ax = plt.subplots(figsize=(5,6))
    im = ax.pcolormesh(Re, eD, 100 * (f_sj - f_cw)/f_cw, cmap='PiYG', vmin=-2, vmax=2)
    plt.colorbar(im, format=PercentFormatter(decimals=1), shrink=0.5, label="Percent error", orientation='horizontal', location='top')
    ax.set_xlabel(r"Reynolds number -- $R_e$")
    ax.set_ylabel(r"Relative pipe roughness -- $e/D$")
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig

if __name__ == "__main__":
    main()