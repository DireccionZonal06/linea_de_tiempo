import streamlit as st
from streamlit_timeline import st_timeline
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="Líneas de tiempo", #Título de la página
    page_icon="📊", # Ícono
    layout="wide", # Forma de layout ancho o compacto
    initial_sidebar_state="expanded" # Definimos si el sidebar aparece expandido o colapsado
)

dfDatos=pd.read_csv("historial_estaciones.csv")
#st.dataframe(dfDatos)

# Validamos que existan datos para generar la línea de tiempo
if len(dfDatos.dropna()) > 0:
    items=[]
    columns=dfDatos.columns
    item={}

    for indice, fila in dfDatos.iterrows():      
        item["style"]=""
        for col in columns: 
            if fila[col]:
                if col == "color":
                    color=fila["color"]
                    item["style"]= f"background-color:{color};" + item["style"]
                elif col == "textcolor":
                    color =fila["textcolor"]
                    item["style"]= f"color:{color};" + item["style"]
                elif col == "title":
                    item["title"] =fila["start"]
                elif col=="content":
                    item["content"] =fila["title"]
                else:
                    item[col] = fila[col]                    
        item["id"] = indice # Adicionamos el id
        items.append(item) # Adicionamos el item al array
        item ={} # Reinicializamos la variable

    # Calculamos las fechas iniciales y finales
    FechaMin = (pd.to_datetime(dfDatos["start"]).min()+timedelta(days=-365)).strftime('%Y-%m-%d')
    FechaMax = (pd.to_datetime(dfDatos["start"]).max()+timedelta(days=365)).strftime('%Y-%m-%d')
 

    st.header("Historial de Mantenimientos en Estaciones Automáticas DZ6 - 2025")
    parAltoTimeline = st.slider("Alto de gráfico",min_value=500,step=100,max_value=1800)
    #items = [
    #    {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
    #    {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
    #    {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
    #    {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
    #    {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
    #    {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
    #]

     # Mostramos los resultados
    c1, c2 = st.columns([7,3])
    with c1:
        # Generamos la línea de tiempo retornando el valor seleccionado a la variable timeline
        timeline = st_timeline(items, groups=[], options={}, height=f"{parAltoTimeline}px", width="100%")
    with c2:
        # Validamos si se seleccionó un evento
        if timeline:
            # Buscamos el evento con el id
            dfEvento = dfDatos.iloc[timeline["id"]]
            # Armamos el texto para mostrar
            if (dfEvento['sensor_r_1'] != " " and dfEvento['sensor_i_1'] != " " and dfEvento['sensor_r_2'] != " "):
                 detalleEvento = f"""
                                #### {dfEvento['title']}
                                **Fecha**: {dfEvento['start']}\n\n
                                {dfEvento['content']}\n
                                **Sensor Instalado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_i_1']} | {dfEvento['marca_i_1']} |  {dfEvento['modelo_i_1']}  | {dfEvento['serie_i_1']}  |
                                
                                 **Sensor Reemplazado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_r_1']} | {dfEvento['marca_r_1']} |  {dfEvento['modelo_r_1']}  | {dfEvento['serie_r_1']}  |
                                | {dfEvento['sensor_r_2']} | {dfEvento['marca_r_2']} |  {dfEvento['modelo_r_2']}  | {dfEvento['serie_r_2']}  |
                """

            elif (dfEvento['sensor_r_1'] != " " and dfEvento['sensor_i_1'] != " "):
                 detalleEvento = f"""
                                #### {dfEvento['title']}
                                **Fecha**: {dfEvento['start']}\n\n
                                {dfEvento['content']}\n
                                **Sensor Instalado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_i_1']} | {dfEvento['marca_i_1']} |  {dfEvento['modelo_i_1']}  | {dfEvento['serie_i_1']}  |\n
                                 **Sensor Reemplazado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_r_1']} | {dfEvento['marca_r_1']} |  {dfEvento['modelo_r_1']}  | {dfEvento['serie_r_1']}  |
                """
            elif dfEvento['sensor_r_1'] != " ":

                detalleEvento = f"""
                                #### {dfEvento['title']}
                                **Fecha**: {dfEvento['start']}\n\n
                                {dfEvento['content']}\n
                                **Sensor Reemplazado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_r_1']} | {dfEvento['marca_r_1']} |  {dfEvento['modelo_r_1']}  | {dfEvento['serie_r_1']}  |
                                
                """
            elif dfEvento['sensor_i_1'] != " ":
                 detalleEvento = f"""
                                #### {dfEvento['title']}
                                **Fecha**: {dfEvento['start']}\n\n
                                {dfEvento['content']}\n
                                **Sensor Instalado**
                                | Sensor        | Marca  | Modelo | Serie |
                                |---------------|--------|--------|-------|
                                | {dfEvento['sensor_i_1']} | {dfEvento['marca_i_1']} |  {dfEvento['modelo_i_1']}  | {dfEvento['serie_i_1']}  |
                                
                """
            
            else:
                detalleEvento = f"""
                                #### {dfEvento['title']}
                                **Fecha**: {dfEvento['start']}\n\n
                                {dfEvento['content']}\n
                                
                """
            # Mostramos los detalles del evento seleccionado
            st.write(detalleEvento,unsafe_allow_html=True)

    #st.dataframe(dfDatos)
    dfData=dfDatos
    dfData["title"]=dfData["title"].str.split('-', expand=False)
    #titulo.columns = ['first_name', 'last_name']
    #df = pd.concat([dfData, titulo], axis=1)
    st.dataframe(dfData)
