

from asyncio import subprocess
import base64
from socket import timeout
import csv_handler as ch
import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import UIsupport as ui
import concurrent.futures
from streamlit_ace import st_ace
from multiprocessing import Process
import os
from decimal import Decimal



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

if 'loadinggif' not in st.session_state:
     loadinggif = st.empty()


     






# st.write(st.session_state)
file = 'run.py'


# if st.button('test'):
#      ui.storeStrintoPy(string=Input,filename=file)

col1, col2 ,col3= st.columns([1,2,3])

agree = col1.checkbox('Live Chart')

if agree:
     if 'live' not in st.session_state:
          live = True
     st.session_state['live'] = True
     st.session_state['delay'] = col2.select_slider('Set animation speed(sec)', options=np.arange(Decimal('0.01'), Decimal('1'), Decimal('0.01')))
else:
     if 'live' not in st.session_state:
          live = False
     st.session_state['live'] = False

# def test():
#      ui.loading('static/loading.gif')


#start to initialize the chart
if st.button('Run simulator'):
     st.session_state['loading'] = False
     ch.clean_cache(ch.CACHE)
     ui.storeStrintoPy(string=Input,filename=ch.FILE)
     ui.loading(ui.LOADING_GIF)
     if ch.check_exists(ch.INFRASTRUCTURE,ch.APPLICATION) == 2:
          if st.session_state.live == False:
               inf_df = pd.read_csv(ch.CACHE+ch.INFRASTRUCTURE,index_col=0)
               infrastructure.line_chart(data=inf_df,width=500,height=500)
               app_df = pd.read_csv(ch.CACHE+ch.APPLICATION,index_col=0)
               application.line_chart(data=app_df,width=500,height=500)
          else:
               inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
               inf_chart = infrastructure.line_chart(data=inf_df,width=500,height=500)
               app_df = ch.read_first_line(ch.APPLICATION)
               app_chart = application.line_chart(data=app_df,width=500,height=500)
               for i in range(1,ch.get_row_length(ch.INFRASTRUCTURE)):
                    inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE,nrows=i))
                    time.sleep(float(st.session_state.delay)/2)
               for i in range(1,ch.get_row_length(ch.APPLICATION)):
                    app_chart.add_rows(ch.read_row_by_sequence(ch.APPLICATION,nrows=i))
                    time.sleep(float(st.session_state.delay)/2)
          st.success('Done!')
     elif ch.check_exists(ch.INFRASTRUCTURE,ch.APPLICATION) == 1:
          if st.session_state.live == False:
               inf_df = pd.read_csv(ch.CACHE+ch.INFRASTRUCTURE,index_col=0)
               st.line_chart(data=inf_df)
          else:
               inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
               inf_chart = st.line_chart(data=inf_df,width=500,height=500)
               for i in range(1,ch.get_row_length(ch.INFRASTRUCTURE)):
                    inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE,nrows=i))
                    time.sleep(float(st.session_state.delay))
          st.success('Done!')
     else:
          st.error('''Please input valid code so that the LEAF simulator can output results.
                Check About for more detail.''')
          st.empty()
     ui.loading('static/loading.gif')

     #TODO
     #st.progress


 
     






st.markdown('''
     <style>
     #leaf > div > span{ color: green;} 
     #application > div > span{color: green;} 

     #root > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-flex-end > button > span{MuiButton-label:"test"}
     </style>''', unsafe_allow_html=True)