# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 12:28:14 2023

@author: moura

"""

import pandas as pd
import streamlit as st

w = st.file_uploader("Upload a CSV file", type="csv")
if w:
    df = pd.read_csv(w)
    st.write(df)

paises = list(df['location'].unique());

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

dtini = st.sidebar.selectbox('Escolha a data inicial', ['Todos'] + paises);
dtfim = st.sidebar.selectbox('Escolha a data final', ['Todas'] + paises);

dtreceb = st.sidebar.selectbox('Escolha a data final', ['Todas'] + paises);

if(dtini != 'Todos'):
    st.header('Mostrando resultados de ' + dtini);
    df = df[df['location']== dtini]
else:
    st.header('Mostrando resultados para todos os países ');
    
dfShow = df.groupby(by = ['date']).sum()


# rodar no terminal
# streamlit run streamly_example2.py