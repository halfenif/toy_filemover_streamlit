import streamlit as st
from datetime import date
import pandas as pd
import random
import numpy as np


@st.cache_data
def get_data():
    return pd.DataFrame(
        {
            "categorical": np.random.choice(
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"], 30
            ),
            "date": np.random.choice(
                pd.date_range(date(2023, 7, 1), date(2023, 7, 31)), 30
            ),
            "numerical": np.random.randint(1, 10, 30),
            "bool": np.random.choice([True, False], 30),
        }
    )


if "data" not in st.session_state:
    df = get_data()
    df["select"] = False
    st.session_state["data"] = df

if "editor_key" not in st.session_state:
    st.session_state["editor_key"] = random.randint(0, 100000)

if "last_selected_row" not in st.session_state:
    st.session_state["last_selected_row"] = None


def get_row_and_clear_selection():
    key = st.session_state["editor_key"]
    df = st.session_state["data"]
    selected_rows = st.session_state[key]["edited_rows"]
    print(selected_rows)
    selected_rows = [int(row) for row in selected_rows if selected_rows[row]["select"]]
    try:
        last_row = selected_rows[-1]
    except IndexError:
        return
    df["select"] = False
    st.session_state["data"] = df
    st.session_state["editor_key"] = random.randint(0, 100000)
    st.session_state["last_selected_row"] = df.iloc[last_row]
    st.session_state["data"].loc[last_row, "select"] = True
    st.session_state["last_selected_row_index"] = last_row


st.data_editor(
    st.session_state["data"],
    key=st.session_state["editor_key"],
    on_change=get_row_and_clear_selection,
)


def update_row():
    idx = st.session_state["last_selected_row_index"]

    st.session_state["data"].loc[idx, "categorical"] = st.session_state["prueba_text"]
    st.session_state["data"].loc[idx, "numerical"] = st.session_state["prueba_number"]
    st.session_state["data"].loc[idx, "bool"] = st.session_state["prueba"]
    st.session_state["data"].loc[idx, "date"] = str(st.session_state["prueba_date"])


last_row = st.session_state["last_selected_row"]

if last_row is not None:
    st.write("Last selected row:", last_row)
    st.write("Do something with that data...")

    st.checkbox("Prueba", value=last_row["bool"], key="prueba")
    st.number_input("Prueba Number", value=last_row["numerical"], key="prueba_number")
    st.text_input("Prueba Text", value=last_row["categorical"], key="prueba_text")
    st.date_input("Prueba Date", value=last_row["date"], key="prueba_date")

    st.button("Modify", on_click=update_row)