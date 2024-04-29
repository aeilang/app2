import copy
import json
import time
import streamlit as st
from googletrans import Translator
import random
import pandas as pd

city = pd.read_csv("./streamlit-prettymapp/univercity.csv")

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
name = EXAMPLES["Macau"]["address"]

def repeat(name):
    
    st.write(name)

    draw_settings = copy.deepcopy(STYLES["Peach"])

    translator = Translator()
    col2.form_submit_button(label="提交")

    result_container = st.empty()
    # fine
    with st.spinner("正在制作地图，可能需要1分钟"):
        result = translator.translate(name, dest='en')
        try:
            aoi = get_aoi(address=result.text, radius=1100, rectangular=False)
        except:
            st.error(f"地名错误，请更换地名 {result.text}")
            st.stop()
        df = st_get_osm_geometries(aoi=aoi)
        config = {
            "aoi_bounds": aoi.bounds,
            "draw_settings": draw_settings,
            "name_on": False,
            "name": name,
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
    st.session_state["previous_style"] = "Peach" 

    time_rand = random.randint(20, 40)
    time.sleep(time_rand)
    random_number = random.randint(1, 140)
    name = city['unuversity'][random_number-1]
    name = name.strip()
    return name
    
    

while True:
    name = repeat(name=name)
