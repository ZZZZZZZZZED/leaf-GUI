
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

#title
st.title('LEAF')

#input box title
st.markdown("###  Python Input")

#input box
Input = st_ace(language = 'python', theme='xcode',key="code input",auto_update=True,max_lines=20,font_size=22)

#chart layout spaceholder
infrastructure, application = st.columns(2)
infrastructure.empty()
application.empty()

#initialize empty charts
empty_list = []
zero = 0.0
columns=''
empty_list.append(zero)
df = pd.DataFrame(empty_list,index=[zero],columns=[columns])


if st.button('test'):
     UIsupport.testing()






st.write(st.session_state)


#start to initialize the chart
if st.button('Run simulator'):
     if 'inf_chart' not in st.session_state:
          st.session_state['inf_chart'] = infrastructure.line_chart(data=df,width=500)
     # else:
     #      st.session_state.inf_chart
     
     UIsupport.read_logs_update_chart_test()

     st.write(st.session_state)
     # UIsupport.storeStrintoPy(str=Input,filename="run.py")
     # os.system("python run.py")
     

     






st.markdown('''
     <style>
     #infrastructure > div > span{ color: green;} 
     #application > div > span{color: green;} 
     #root > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-flex-end > button > span{MuiButton-label:"test"}
     </style>''', unsafe_allow_html=True)