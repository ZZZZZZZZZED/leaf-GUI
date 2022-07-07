
from email.utils import decode_rfc2231
import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import UIsupport
import simpy

from streamlit_ace import st_ace
import global_var
import os



st.set_page_config(
     page_title="LEAF - Simulator User Interface",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "What is LEAF: https://leaf.readthedocs.io/en/latest/"
     }
)





st.title('LEAF') #homepage maintitle
st.markdown("###  Python Input")

Input = st_ace(language = 'python', theme='xcode',key="code input",auto_update=True,max_lines=20,font_size=22)



infrastructure, application = st.columns(2)
infrastructure.empty()
application.empty()



# app_chart = application.line_chart(np.random.randn(20, 1),width=500)
temp_list = []
num = 0

temp_list.append(num)



df2 = pd.DataFrame([1],index=[1],columns=['test'])

ss = st.session_state
if 'j' not in st.session_state:
     st.session_state['j'] = 0
if 'temp_list' not in st.session_state:
     st.session_state['temp_list'] = temp_list

st.dataframe(df2)


df3 = pd.DataFrame(temp_list[0]-1,index=[0],columns=['columns'])
df4 = pd.DataFrame(temp_list[0]-20,index=[5],columns=['columns'])
st.dataframe(df3)

st.write(st.session_state)

# if st.button('test add'):
#      infrastructure, application = st.columns(2)
#      st.session_state['temp_list'][0] -= 1
#      df3 = pd.DataFrame(st.session_state.temp_list[0],index=[st.session_state.j],columns=['columns'])
#      st.session_state['inf_chart'].add_rows(df3)
     
#      # UIsupport.draw_infrastructure(temp_list,i=[st.session_state.j],columns=['test'])
#      st.session_state['j']+=1
#      # st.session_state['inf_chart'].add_rows(df2)





df = pd.DataFrame(temp_list,index=[0],columns=[''])
st.dataframe(df)

if st.button('Run simulator'):
     if 'inf_chart' not in st.session_state:
          st.session_state['inf_chart'] = infrastructure.line_chart(data=df,width=500)
     st.session_state['inf_chart'].add_rows(df2)
     st.session_state['inf_chart'].add_rows(df3)
     st.session_state['inf_chart'].add_rows(df4)
     for i in range(10):
          time.sleep(0.5)
          st.session_state['inf_chart'].add_rows(df4)
     st.write(st.session_state)
     UIsupport.storeStrintoPy(str=Input,filename="run.py")
     os.system("python run.py")
     

     






st.markdown('''
     <style>
     #infrastructure > div > span{ color: green;} 
     #application > div > span{color: green;} 
     #root > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-flex-end > button > span{MuiButton-label:"test"}
     </style>''', unsafe_allow_html=True)