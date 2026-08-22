import datetime as dt
import streamlit as st
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine

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
st.title("Kitting & Reception download")

df = pd.read_sql("SELECT * FROM reception", con=engine)
after_inv_df = pd.read_sql("SELECT * FROM reception  WHERE reception_date > '2026-05-17' ", con=engine)

buffer = BytesIO()
after_inv_buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False)

with pd.ExcelWriter(after_inv_buffer, engine="xlsxwriter") as writer:
    after_inv_df.to_excel(writer, index=False)

st.download_button(
    label="📥 Download reception history",
    data=buffer.getvalue(),
    file_name=f"reception_history_{dt.datetime.now():%Y%m%d_%H%M%S}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

############################ kitting archive ##################################

df_kit = pd.read_sql("SELECT * FROM kitting", con=engine)
buffer_kit = BytesIO()
with pd.ExcelWriter(buffer_kit, engine="xlsxwriter") as writer:
    df_kit.to_excel(writer, index=False)



st.download_button(
    label="📥 Download kitting archive",
    data=buffer_kit.getvalue(),
    file_name=f"kitting_archive_{dt.datetime.now():%Y%m%d_%H%M%S}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

############################ kit_todo archive ##################################

df_kit2 = pd.read_sql("SELECT * FROM kit_todo", con=engine)
buffer_kit2 = BytesIO()
with pd.ExcelWriter(buffer_kit2, engine="xlsxwriter") as writer:
    df_kit2.to_excel(writer, index=False)



st.download_button(
    label="📥 Download kit_todo archive",
    data=buffer_kit2.getvalue(),
    file_name=f"kit_todo_archive_{dt.datetime.now():%Y%m%d_%H%M%S}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.image("pks_v2/logo-38023-scaled.jpg")
