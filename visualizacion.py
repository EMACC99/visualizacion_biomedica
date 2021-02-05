import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

@st.cache(persist=True)
def load_dataset(filename : str, **kargs):
    data = pd.read_csv(filename, **kargs)
    return data

st.title('Visualizacion de datos sobre IA en investigacion biomedica en Mexico')
st.sidebar.title('Visualizacion de datos sobre IA en investigacion biomedica en Mexico')


dataset = st.sidebar.selectbox('Dataset', ['BioMedica', 'Procesamiento Natural de Lenguaje'])

filename = 'Datasets/bio_mex_papers_2.csv'

if dataset == 'BioMedica':
    filename = 'Datasets/bio_mex_papers_2.csv'
elif dataset == 'Procesamiento Natural de Lenguaje':
    filename =  'Datasets/dataset_del_fer.csv'


dataset = load_dataset(filename)
institutos = load_dataset('Datasets/institutos.csv')

st.sidebar.markdown('Paper random por cantidad de mujeres')
cant_mujeres = st.sidebar.slider('Cantidad de Mujeres', min_value=1, max_value=4)
st.sidebar.markdown(dataset[dataset['cantidad de mujeres'].apply(lambda x : x  == cant_mujeres)][['Año', 'Título']].sample(n=1).values[0])
st.markdown('## Conteo de mujeres por paper')

mujeres_count = dataset['cantidad de mujeres'].value_counts()
cant_mujeres = pd.DataFrame({'cant' : mujeres_count.index, 'value': mujeres_count.values})
fig = px.bar(cant_mujeres, x = 'cant', y = 'value', height = 500)
st.plotly_chart(fig)

st.markdown('## Mujeres por año')
anios = sorted(dataset['Año'].unique())
cantidad_mujeres_anio = []
for anio in anios:
    cantidad_mujeres_anio.append(sum(dataset[dataset['Año'] == anio]['cantidad de mujeres']))
fig = px.scatter(x = anios, y = cantidad_mujeres_anio)
st.plotly_chart(fig)

num_institutos = st.sidebar.slider('Top de institutos', min_value = 5, max_value = len(institutos))
institutos.sort_values('Count', ascending=False, inplace=True)
st.markdown(f'## Top {num_institutos} de institutos por publicacion registrada')
fig = px.bar(institutos[:num_institutos], x = 'Instituto', y = 'Count')
st.plotly_chart(fig)
