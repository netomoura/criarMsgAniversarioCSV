# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 12:28:14 2023

@author: moura

"""

import pandas as pd
import streamlit as st
import datetime

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
    
def retornaTexto(nome, dtAniver, email, dtRec, dtAniverStr):
    
    #dtAniverDT = dtAniver.to_pydatetime()
    #dtAniverSt = dtAniver.strftime('%Y-%m-%d')
    #dtRecSt = dtRec.strftime('%Y-%m-%d')
    
    primeiroNome=nome.split()[0]
    text = "<hr><p><b>Nome: " + nome + "</b>"
    text += "</p><p>Dia Aniversário: " + dtAniverStr
    text += "</p><p>E-mail: " + email
    text += "</p><p>Assunto: Feliz Aniversário</p>" 
    text += "<br>"     
    text += "<p><b>Mensagem:</b>"     
    text += "<p>Parabéns " + primeiroNome.capitalize() + ","
    
    #if nome == "MARISA DE CAMARGO":
    #if dtAniverSt == dtRecSt:
    if tOn:        
        text += "</p><p>Neste dia tão especial, desejo-lhe muita paz, alegria e que seu novo ciclo seja repleto de saúde, sucesso e felicidades!</p>"    
    else:
        text += "</p><p>Espero que este dia tão especial tenha sido repleto de muita paz e alegria. Que seu novo ciclo seja cheio de saúde, sucesso e felicidades!</p>"
    
    text += "<p>Obrigado pelo seu trabalho na SAM.</p>"
    text += "<p></p>"
    text += "<p>Atenciosamente,</p><br>"
    text += "<p></p>"
    text += "<p>Alessandro Dintof</p>"
    text += "<p>SAM-GAB</p>"
    return text

w = st.file_uploader("Faça o upload do seu arquivo CSV", type="csv")
if w:
    df = pd.read_csv(w, encoding="iso8859-1")
    
    #nome = st.sidebar.text_input('Nome')
    dtIni = st.sidebar.date_input("Selecione a data inicial", value="today", format="DD/MM/YYYY")
    dtFim = st.sidebar.date_input("Selecione a data final", value="today", format="DD/MM/YYYY")
    tOn = st.sidebar.toggle('No dia')
    #dtRec = st.sidebar.date_input("Selecione a data de recebimento", datetime.date(2023, 7, 12), format="DD/MM/YYYY")
    #dtRec = st.sidebar.date_input("Selecione a data de recebimento", value="today", format="DD/MM/YYYY")    
        
    df['dtAniver'] = pd.to_datetime(df['Data de Aniversário']+"/2023")
    df['dtIni'] = dtIni
    df['dtFim'] = dtFim
    #df['dtRec'] = dtRec
    df['cond'] = (df['dtFim'] >= df['dtAniver']) & (df['dtIni'] <= df['dtAniver'])
    
    #if(nome != ''):
     #   df = df[df['Nome'] == nome]

    for i, row_i in df.iterrows():
        if row_i['cond'] == True:
            st.write(retornaTexto(row_i['Nome'], row_i['dtAniver'], row_i['E-mail'], "", row_i['Data de Aniversário']), unsafe_allow_html=True)  
        
    #for index, row in df.iterrows():
        #print(row['Nome'], row['condini']) 
    
else:
    
    st.header('Escolha seu arquivo para iniciar o processo!');
    
    #df = load_data();

    # rodar no terminal
    # streamlit run criarMsgAniversarioCSV.py
    
    