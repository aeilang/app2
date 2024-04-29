import copy
import json

import streamlit as st
from googletrans import Translator

from utils import (
    st_get_osm_geometries,
    st_plot_all,
    get_colors_from_style,
)
from prettymapp.geo import GeoCodingError, get_aoi
from prettymapp.settings import STYLES

st.set_page_config(
    page_title="prettymapp", page_icon="🖼️", initial_sidebar_state="collapsed"
)


with open("./streamlit-prettymapp/examples.json", "r", encoding="utf8") as f:
    EXAMPLES = json.load(f)

if not st.session_state:
    st.session_state.update(EXAMPLES["Macau"])

    lc_class_colors = get_colors_from_style("Peach")
    st.session_state.lc_classes = list(lc_class_colors.keys())  # type: ignore
    st.session_state.update(lc_class_colors)
    st.session_state["previous_style"] = "Peach"
    st.session_state["previous_example_index"] = 0



st.write("")
form = st.form(key="form_settings")
col1, col2, col3 = form.columns([3, 1, 1])

address = col1.text_input(
    "地址",
    key="address",
)


draw_settings = copy.deepcopy(STYLES["Peach"])

translator = Translator()
col3.form_submit_button(label="提交")



result_container = st.empty()
with st.spinner("正在制作地图，可能需要1分钟"):
    result = translator.translate(address, dest='en')
    try:
        aoi = get_aoi(address=result.text, radius=1500, rectangular=False)
    except:
        st.error(f"地名错误，请更换地名 {result.text}")
        st.stop()
    df = st_get_osm_geometries(aoi=aoi)
    config = {
        "aoi_bounds": aoi.bounds,
        "draw_settings": draw_settings,
        "name_on": False,
        "name": address,
        "font_size": 25,
        "font_color": "#2F3737",
        "text_x": 19,
        "text_y": -45,
        "text_rotation": 0,
        "shape": "circle",
        "contour_width": 1,
        "contour_color": "#2F3537",
        "bg_shape": "circle",
        "bg_buffer": 2,
        "bg_color": "#F2F4CB",
    }
    fig = st_plot_all(_df=df, **config)
    # result_container.write(html, unsafe_allow_html=True)
    st.pyplot(fig, pad_inches=0, bbox_inches="tight", transparent=True, dpi=300)


