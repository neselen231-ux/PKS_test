import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import re
import os
from barcode.codex import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import zipfile
import socket
import treepoem





hide_ui = """
<style>
#MainMenu {visibility: hidden;}      /* 메뉴 */
header {visibility: hidden;}         /* 헤더 */
footer {visibility: hidden;}         /* Footer */

div[data-testid="stStatusWidget"] {display: none;}   /* status badge */
div[data-testid="stDecoration"] {display: none;}     /* hosted badge */
div.viewerBadge_link__1S137 {display: none;}         /* created by */
</style>
"""
st.markdown(hide_ui, unsafe_allow_html=True)

engine = create_engine(
    f"mysql+pymysql://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}",
    connect_args={
        "ssl": {"ca": "ca.pem"}
    }
)
st.title("PFE kitting input")

# 2 input boxes

with st.form("input_form"):
    Project = st.selectbox("Project",
    ["ALS105","ALS525", "H3P","H4P", "SIEMENS","Rework"])
    Pack_number = st.text_input("Pack_number", "1")
    kit_name = st.text_input("kit_name")
    Product = st.text_input("Product")
    submit = st.form_submit_button("Input")


if submit:
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO kit_todo
                    (Project, Pack_number, kit_name, Product)
                VALUES
                    (:prj, :pnm, :kitn, :pro)
            """),
            {
                "prj": Project,
                "pnm": Pack_number,
                "kitn": kit_name,
                "pro": Product
            }
        )
    st.success("DB updated")                        

   
