from turtle import color
import pandas as pd
import plotly.express as px
import streamlit as st

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Torre Control", page_icon=":vertical_traffic_light:", layout="wide")

# ---- READ EXCEL ----
def get_data_from_excel():
    df = pd.read_excel(
        io="torreControl.xlsx",
        engine="openpyxl",
        sheet_name="Y_DEV_420000074",
        usecols="A:AB",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["HLiq"] = pd.to_datetime(df["HLiq"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Filtros:")
zonadist = st.sidebar.multiselect(
    "Selecciona la zona de Dist:",
    options=df["Zona"].unique(),
    default=df["Zona"].unique()
)

numViaje = st.sidebar.multiselect(
    "Seleccione el número de viaje:",
    options=df["group_trip"].unique(),
    default=df["group_trip"].unique(),
)

Liquida2 = st.sidebar.multiselect(
    "Consulta de Liquidación:",
    options=df["Liquida2"].unique(),
    default=df["Liquida2"].unique()
)

enRuta = st.sidebar.multiselect(
    "Consulta de pendientes de salir a Ruta:",
    options=df["En_Ruta"].unique(),
    default=df["En_Ruta"].unique()
)

df_selection = df.query(
    "Zona == @zonadist & group_trip == @numViaje & Liquida2 == @Liquida2 & En_Ruta == @enRuta"
)

# ---- MAINPAGE ----
st.title(":articulated_lorry: Rutas de Distribución")
st.markdown("##")

# TOP KPI's
total_ruta = int(df_selection["Guia"].count())
primeros_viajes = int(df_selection.groupby(by=["group_trip"]).count()["Guia"].max())
segundos_viajes = int(df_selection.groupby(by=["group_trip"]).count()["Guia"].min())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de Viajes:")
    st.subheader(f"{total_ruta:,}")
with middle_column:
    st.subheader("Primeros Viajes:")
    st.subheader(f"{primeros_viajes}")
with right_column:
    st.subheader("Segundos Viajes:")
    st.subheader(f"{segundos_viajes}")

st.markdown("""---""")


# SALES BY HOUR [BAR CHART]
total_rutas_zona = (df_selection.groupby(by=["Zona"]).count()[["Guia"]].sort_values(by="Guia"))
fig_total_rutas_zona = px.bar(
    total_rutas_zona,
    x=total_rutas_zona.index,
    y="Guia",
    color="Guia",
    title="Total de Rutas por Zona",
)
fig_total_rutas_zona.update_layout(
    xaxis_title="Zona",
    yaxis_title="Total de Rutas",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
st.plotly_chart(fig_total_rutas_zona, use_container_width=True)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)