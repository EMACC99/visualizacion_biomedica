import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

@st.cache(persist=True)
def load_dataset(filename : str, **kargs):
    data = pd.read_csv(filename, **kargs)
    return data

st.title('Visualización de datos sobre IA en investigación biomédica en México')
st.sidebar.title('Visualización de datos sobre IA en investigación biomédica en México')


dataset = st.sidebar.selectbox('Dataset', ['BioMedica', 'Procesamiento Natural de Lenguaje'], key = '0')

filename = 'Datasets/biomed_1.csv'

if dataset == 'BioMedica':
    filename = 'Datasets/biomed_1.csv'
    columna = 'pacientes mexicanos'
elif dataset == 'Procesamiento Natural de Lenguaje':
    filename =  'Datasets/dataset_del_fer.csv'
    columna = 'columna del fer'

dataset = load_dataset(filename)
institutos = load_dataset('Datasets/institutos_rev_1.csv')

st.sidebar.markdown('Paper random por cantidad de mujeres')
cant_mujeres = st.sidebar.slider('Cantidad de Mujeres', min_value=1, max_value=4)
st.sidebar.markdown(dataset[dataset['cantidad de mujeres'].apply(lambda x : x  == cant_mujeres)][['Año', 'Título']].sample(n=1).values[0])
st.markdown('## Conteo de mujeres por paper')

mujeres_count = dataset['cantidad de mujeres'].value_counts()
cant_mujeres = pd.DataFrame({'cant' : mujeres_count.index, 'value': mujeres_count.values})
fig = px.bar(cant_mujeres, x = 'cant', y = 'value', height = 500)
st.plotly_chart(fig)

st.markdown('## Posiciones de las autoras en los papers')
mujeres = dataset['¿Mujeres?'].values
positions = {}
for position in mujeres:
    position = position.split(';')
    for key in position:
        if key != '0':
            if key in positions:
                positions[key] += 1
            else:
                positions[key] = 1
positions = pd.DataFrame(positions.items(), columns=['position', 'count'])
fig = px.bar(positions.sort_values('position'), x = 'position', y = 'count')
st.plotly_chart(fig)

proporcion_autores = []
autores_count = 0
autores = dataset.Autores.values
for autore in autores:
    autore = autore.split(';')
    autore_size = len(autore)
    proporcion_autores.append(autore_size)
    autores_count += autore_size
proporcion_autores = dataset['cantidad de mujeres'].values/proporcion_autores

st.markdown(f'## De los papers registrados, en promedio la relacion autor:autora es de {proporcion_autores.mean()}')

st.markdown('## Mujeres por año')
anios = sorted(dataset['Año'].unique())
cantidad_mujeres_anio = []
for anio in anios:
    cantidad_mujeres_anio.append(sum(dataset[dataset['Año'] == anio]['cantidad de mujeres']))
fig = px.scatter(x = anios, y = cantidad_mujeres_anio)
st.plotly_chart(fig)

num_institutos = st.sidebar.slider('Top de institutos', min_value = 5, max_value = len(institutos))
institutos.sort_values('Count', ascending=False, inplace=True)
st.markdown(f'## Top {num_institutos} de institutos por publicación registrada')
fig = px.bar(institutos[:num_institutos], x = 'Instituto', y = 'Count')
st.plotly_chart(fig)

st.markdown('## Papers por Año')
papers_por_anio = dataset['Año'].value_counts()
papers_por_anio = pd.DataFrame({'Año': papers_por_anio.index, 'value': papers_por_anio.values})
fig =  px.bar(papers_por_anio, x = 'Año', y = 'value')
st.plotly_chart(fig)


st.markdown('# Datasets')

st.markdown('## Porcetage de Datasets Registrados con pacientes de personas Mexicanas y no Mexicanas')
pacientes = dataset[columna].iloc[:-1]
pacientes_count = {}
for paciente in pacientes.values:
    paciente = paciente.split(';')
    for item in paciente:
        item = item.lower()
        if item in pacientes_count:
            pacientes_count[item] += 1
        else:
            pacientes_count[item] = 1

pacientes_df = pd.DataFrame(pacientes_count.items(), columns=['value', 'count'])
fig = px.pie(pacientes_df, names = 'value', values = 'count')
st.plotly_chart(fig)


st.markdown('## Datos Reales o ficticios')
reales_ficticios = dataset['reales/ficticios'].iloc[:-1]
reales_ficticios_count = {}
for dato in reales_ficticios.values:
    dato = dato.split(';')
    for item in dato:
        item = item.lower()
        if item in reales_ficticios_count:
            reales_ficticios_count[item] += 1
        else:
            reales_ficticios_count[item] = 1

reales_ficticios_df = pd.DataFrame(reales_ficticios_count.items(), columns=['value', 'count'])
fig = px.pie(reales_ficticios_df, names = 'value', values = 'count')
st.plotly_chart(fig)

st.markdown('## Creados o de otro lado')
de_donde = dataset['de donde'].values[:-1]
count_datasets = {}
for datasets in de_donde:
    datasets = datasets.split(';')
    for dataset in datasets:
        dataset = dataset.rstrip().lstrip()
        if dataset in count_datasets:
            count_datasets[dataset] += 1
        else:
            count_datasets[dataset] = 1

creados, otros = 0,0
for item in count_datasets:
    if item == 'creado':
        creados += count_datasets[item]
    else:
        otros += count_datasets[item]

creados_o_relaes = {'creado' : creados, 'reales': otros}

creados_o_relaes = pd.DataFrame(creados_o_relaes.items(), columns=['tipo', 'count'])

fig = px.pie(creados_o_relaes, names = 'tipo', values = 'count')
st.plotly_chart(fig)