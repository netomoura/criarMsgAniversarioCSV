# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 12:28:14 2023

@author: moura

"""

import pandas as pd
import streamlit as st
import datetime

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# Cache the dataframe so it's only loaded once
@st.cache_data
def load_data():
    #return pd.DataFrame(
    #    {
    #        "first column": [1, 2, 3, 4],
    #        "second column": [10, 20, 30, 40],
    #    }
    #)
    return pd.read_csv('../github/aniversarios.csv', encoding="iso8859-1");
    
w = st.file_uploader("Upload a CSV file", type="csv")
if w:
    df = pd.read_csv(w, encoding="iso8859-1")
    #st.dataframe(filter_dataframe(df))
    
    #nome = st.sidebar.text_input('Nome')
    dtIni = st.sidebar.date_input("Selecione a data inicial", datetime.date(2023, 7, 11), format="DD/MM/YYYY")
    dtFim = st.sidebar.date_input("Selecione a data final", datetime.date(2023, 7, 13), format="DD/MM/YYYY")
    dtRec = st.sidebar.date_input("Selecione a data de recebimento", value="today", format="DD/MM/YYYY")
    
    df['dtAniver'] = pd.to_datetime(df['Data de Aniversário']+"/2023")
    df['dtIni'] = dtIni
    df['dtFim'] = dtFim
    df['dtRec'] = dtRec
    df['cond'] = (df['dtFim'] >= df['dtAniver']) & (df['dtIni'] <= df['dtAniver'])
    
    #if(nome != ''):
     #   df = df[df['Nome'] == nome]

    for i, row_i in df.iterrows():
        if row_i['cond'] == True:
            st.write(row_i['Nome'], row_i['dtAniver'], row_i['E-mail'])  
        
    #for index, row in df.iterrows():
        #print(row['Nome'], row['condini']) 
    
else:
    
    st.header('Escolha seu arquivo para iniciar o processo!');
    
    df = load_data();

    # rodar no terminal
    # streamlit run criarMsgAniversarioCSV.py
    
    