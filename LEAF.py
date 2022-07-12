

from asyncio import subprocess
import base64
from socket import timeout

import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import UIsupport
import concurrent.futures
from streamlit_ace import st_ace
from multiprocessing import Process
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

# loadinggif = st.empty()
if 'loadinggif' not in st.session_state:
     loadinggif = st.empty()
# def loading(path):
#      global loadinggif
#      if st.session_state.loading == False:
#           st.session_state['loading'] = True
#           file_ = open(path, "rb")
#           contents = file_.read()
#           data_url = base64.b64encode(contents).decode("utf-8")
#           file_.close()
#           # cols = st.columns(3)
#           # with cols[1]:
#           loadinggif = st.markdown(f'<div style="text-align: center"> <img src="data:image/gif;base64,{data_url}" alt="loading gif"> </div>',unsafe_allow_html=True,)
#      elif st.session_state.loading == True:
#           st.session_state['loading'] = False
#           print('loading false')
#           loadinggif.empty()

     
#initialize empty charts
empty_list = []
zero = 0.0
columns= ''
empty_list.append(zero)
df = pd.DataFrame(empty_list,index=[zero],columns=[columns])





# st.write(st.session_state)
if st.button('test'):
     if 'loading' not in st.session_state:  
          st.session_state['loading'] = False

     UIsupport.testing()




def test():
     UIsupport.loading('static/loading.gif')


#start to initialize the chart

if st.button('Run simulator'):
     # initialize
     st.session_state['inf_chart'] = infrastructure.line_chart(data=df,width=500,height=800) 
     st.session_state['loading'] = False

     
     # st.write(st.session_state)
     file = 'run.py'
     UIsupport.storeStrintoPy(str=Input,filename=file)
     UIsupport.loading('static/loading.gif')
     UIsupport.read_logs_update_chart_test()

 
     








st.markdown('''
     <style>
     #infrastructure > div > span{ color: green;} 
     #application > div > span{color: green;} 
     #root > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-flex-end > button > span{MuiButton-label:"test"}
     </style>''', unsafe_allow_html=True)